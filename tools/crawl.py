#!/usr/bin/env python3
"""Polite stdlib-only crawler: sitemap -> plain-text Markdown files + sources.csv.

Usage:
  python3 tools/crawl.py                 # nebius.com (blog/newsroom/site) + docs.nebius.com
  python3 tools/crawl.py --careers       # also snapshot the Greenhouse job board
"""
import csv
import html
import json
import re
import subprocess
import sys
import time
import urllib.robotparser
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent / "corpus"
UA = "Mozilla/5.0 (PANW-SE account research; contact mikeovu@gmail.com)"
DELAY = {"nebius.com": 3.0, "docs": 1.0, "careers": 1.0}  # seconds between requests, per host
# docs first: nebius.com rate-limits hard and may need a later rerun
SITEMAPS = {
    "docs": "https://docs.nebius.com/sitemap.xml",
    "nebius.com": "https://nebius.com/server-sitemap.xml",
}
# Generated reference docs (CLI/API/Terraform) and legal text add ~1,800 pages and nothing for account research
SKIP = re.compile(r"^https://(docs\.nebius\.com/(cli|rest-api|terraform-provider|legal)|nebius\.com/events)(/|$)")
GREENHOUSE = "https://boards-api.greenhouse.io/v1/boards/nebius/jobs"
US = re.compile(r"United States|\bUSA?\b")
# US roles worth reading in full: they say where sites are and what gear runs there
DETAIL = re.compile(r"data ?cent|facilit|site|network|security|infrastructure|construction|"
                    r"electrical|mechanical|critical|hardware|operations", re.I)


def fetch(url):
    # curl uses the macOS keychain for CAs; python.org builds ship without a CA bundle
    r = subprocess.run(["curl", "-sSfL", "--max-time", "30", "-A", UA, url], capture_output=True)
    if r.returncode:
        raise RuntimeError(r.stderr.decode().strip())
    return r.stdout.decode("utf-8", "replace")


class TextExtractor(HTMLParser):
    """Keeps headings, paragraphs, list items, and table cells; drops chrome."""
    SKIP = {"script", "style", "nav", "header", "footer", "svg", "noscript", "form"}
    BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "tr", "pre", "blockquote", "div", "br"}

    def __init__(self):
        super().__init__()
        self.out, self.skip, self.title, self._in_title = [], 0, "", False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag == "title":
            self._in_title = True
        elif not self.skip:
            if tag in ("h1", "h2", "h3", "h4"):
                self.out.append("\n\n" + "#" * int(tag[1]) + " ")
            elif tag == "li":
                self.out.append("\n- ")
            elif tag in ("td", "th"):
                self.out.append(" | ")
            elif tag in self.BLOCK:
                self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self.skip:
            self.out.append(data)

    def text(self):
        t = "".join(self.out)
        t = re.sub(r"[ \t]+", " ", t)
        return re.sub(r"\n\s*\n\s*\n+", "\n\n", t).strip()


def slug(url):
    p = urlparse(url)
    s = (p.netloc + p.path).strip("/").replace("/", "__")
    return re.sub(r"[^A-Za-z0-9_.-]", "-", s) or "index"


def bucket(source, url):
    if source == "docs":
        return "docs"
    for b in ("blog", "newsroom"):
        if f"/{b}/" in url:
            return b
    return "site"


def sitemap_urls(url):
    """Expands sitemap indexes (<sitemap><loc>) into page URLs."""
    xml = fetch(url)
    locs = re.findall(r"<loc>([^<]+)</loc>", xml)
    if "<sitemapindex" not in xml:
        return locs
    return [u for sm in locs for u in sitemap_urls(sm)]


def page(source, url):
    """Returns (title, text). Docs (Mintlify) serve clean Markdown at <url>.md."""
    if source == "docs":
        md = fetch(url.rstrip("/") + ("/index.md" if urlparse(url).path in ("", "/") else ".md"))
        m = re.search(r"^title:\s*\"?(.+?)\"?\s*$", md, re.M) or re.search(r"^# (.+)$", md, re.M)
        return (m.group(1) if m else url), md.strip()
    ex = TextExtractor()
    ex.feed(fetch(url))
    return ex.title.strip(), ex.text()


def crawl_sitemap(source, sitemap_url, writer):
    rp = urllib.robotparser.RobotFileParser()
    host = urlparse(sitemap_url)
    rp.parse(fetch(f"{host.scheme}://{host.netloc}/robots.txt").splitlines())
    urls = [u for u in sitemap_urls(sitemap_url)
            if not SKIP.match(u) and not re.search(r"\.(png|jpe?g|gif|svg|webp|pdf|mp4)$", u, re.I)]
    # blog/newsroom before everything else so research can start early
    urls.sort(key=lambda u: bucket(source, u) == "site")
    print(f"[{source}] {len(urls)} urls", flush=True)
    blocked = 0
    for i, url in enumerate(urls, 1):
        dest = ROOT / bucket(source, url) / (slug(url) + ".md")
        if dest.exists():
            continue
        if not rp.can_fetch(UA, url):
            print(f"  skip (robots) {url}")
            continue
        time.sleep(DELAY[source])  # before the request, so errors are rate-limited too
        try:
            title, text = page(source, url)
            blocked = 0
        except Exception as e:  # keep going on individual page failures
            print(f"  ERR {url}: {e}", flush=True)
            if re.search(r"error: (403|429)", str(e)):
                # nebius.com's edge starts returning 403 above ~1 req/s; back off, then give up on the host
                blocked += 1
                if blocked >= 5:
                    print(f"[{source}] blocked; stopping. Rerun later to resume.", flush=True)
                    return
                time.sleep(60 * blocked)
            continue
        dest.write_text(f"# {title}\n\nSource: {url}\n\n{text}\n")
        writer.writerow([url, title, dest.relative_to(ROOT), datetime.now(timezone.utc).isoformat(timespec="seconds")])
        if i % 25 == 0:
            print(f"  {i}/{len(urls)}", flush=True)


def snapshot_careers(writer):
    jobs = json.loads(fetch(GREENHOUSE))["jobs"]
    keep = [{"id": j["id"], "title": j["title"], "location": j["location"]["name"],
             "url": j["absolute_url"], "updated_at": j["updated_at"]} for j in jobs]
    us = [j for j in keep if US.search(j["location"])]
    print(f"[careers] {len(keep)} jobs, {len(us)} US", flush=True)
    for j in us:
        if not DETAIL.search(j["title"]):
            continue
        try:
            d = json.loads(fetch(f"{GREENHOUSE}/{j['id']}"))
        except Exception as e:
            print(f"  ERR job {j['id']}: {e}", flush=True)
            continue
        j["departments"] = [x["name"] for x in d.get("departments", [])]
        ex = TextExtractor()
        ex.feed(html.unescape(d["content"]))  # Greenhouse returns entity-escaped HTML
        j["content"] = ex.text()
        time.sleep(DELAY["careers"])
    out = ROOT / "careers" / "greenhouse.json"
    out.write_text(json.dumps({"fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                               "total": len(keep), "us": us, "non_us": [j for j in keep if j not in us]}, indent=2))
    writer.writerow([GREENHOUSE, f"Greenhouse jobs ({len(keep)}, {len(us)} US)", out.relative_to(ROOT),
                     datetime.now(timezone.utc).isoformat(timespec="seconds")])


def main():
    for d in ("docs", "blog", "newsroom", "site", "careers"):
        (ROOT / d).mkdir(parents=True, exist_ok=True)
    csv_path = ROOT / "sources.csv"
    new = not csv_path.exists()
    with csv_path.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["url", "title", "file", "fetched_at"])
        if "--careers" in sys.argv:
            snapshot_careers(w)
            f.flush()
        for source, sm in SITEMAPS.items():
            crawl_sitemap(source, sm, w)
            f.flush()


if __name__ == "__main__":
    main()
