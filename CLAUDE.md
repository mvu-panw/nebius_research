# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Internal PANW account research for **Nebius** (NASDAQ: NBIS, full-stack AI cloud), used by a sales engineer for technical enablement and firewall positioning. It has the same structure as `~/lambda` (the Lambda AI account), plus a **US Strategy** page covering Nebius's US data center build-out and US hiring.

**Deployed publicly:** pushed to the public repo `github.com/mvu-panw/nebius_research` (branch `main`). `.github/workflows/pages.yml` runs two jobs. `check` fails on a broken internal `href`/`src`, or on any non-web file in `site/` (a guard against CSV/JSON/PDF exports leaking). `deploy` publishes only `site/` to GitHub Pages on every push to `main`. Pull requests run `check` only. The repo itself, including `corpus/` and this file, is public too, so the positioning is visible to anyone. One-time manual step: Settings → Pages → Source = "GitHub Actions".

**Never commit internal PANW CRM data.** `Nebius_Inventory_*.csv` (install-base exports) is gitignored. Keep any such data out of `site/` and `corpus/`.

## Layout

| Path | What |
|---|---|
| `site/` | Static 6-page front end: `index`, `us-strategy`, `architecture`, `nvidia-gear`, `positioning`, `resources` |
| `corpus/{docs,blog,newsroom,site}/*.md` | Plain-text crawl of docs.nebius.com and nebius.com from sitemaps. Grep this before searching the web. |
| `corpus/careers/greenhouse.json` | Snapshot of the Greenhouse job board: all jobs, plus full text for US infra/DC/network/security roles |
| `corpus/careers/*.md` | Full text of key security postings. `network-security-engineer-*.md` is the incumbent-vendor evidence. |
| `corpus/ir/` | Q1 and Q2 2026 shareholder letters (PDF plus `pdftotext -layout` output). These are the primary source for site counts and power targets. |
| `corpus/sources.csv` | url, title, local file and fetched_at for every crawled page |
| `tools/crawl.py` | Stdlib-only crawler (respects robots.txt, per-host delays) |

## Commands

```bash
python3 -m http.server 8500 --directory site     # preview the site
python3 -I tools/crawl.py --careers               # refresh corpus + job board (skips files that already exist; delete a file to refetch it)
pdftotext -layout corpus/ir/<letter>.pdf corpus/ir/<letter>.txt   # after adding a new shareholder letter
```

Crawler notes:
- `crawl.py` fetches with `curl` via subprocess on purpose. The python.org Python on this Mac has no CA bundle, so `urllib` fails TLS verification. Don't "fix" this by disabling verification.
- **nebius.com returns 403 above about 1 req/s.** The crawler waits 3 s per request there and stops after 5 consecutive 403/429s. Rerun later to resume. Never run two crawlers at once: that is what triggered the block on Oct 29, 2026. WebFetch is also blocked on nebius.com, so use the Business Wire copy of a press release instead.
- Docs are Mintlify, which serves clean Markdown at `<url>.md`, and the crawler uses that. `cli/`, `rest-api/`, `terraform-provider/` and `legal/` (about 1,800 generated pages) and nebius.com `/events/` are skipped on purpose.

## Site conventions

- **The UI is copied from `~/lambda`**, which was copied from `~/ai_sec_by_design` (Prisma AIRS look: cyan/purple gradient, Inter font). `site/assets/css/styles.css` is that file plus a block at the end marked "Nebius account site additions". The block holds the Lambda additions (`.tag-*` confidence pills, `.prose`, `.two-col`, `.link-grid`/`.link-card`, `.table-wrap`) and the Nebius-only `.stat-row`/`.stat` and `.timeline`.
- **No templating:** the nav and footer are copy-pasted into all 6 pages. Each page's `.nav-links` lists the *other* pages, with Home on every page except `index.html`. Edit all 6 files when changing the nav.
- The stylesheet is linked as `styles.css?v=1`. Bump it on every page together after CSS edits.
- **Every factual claim carries a source link and a confidence tag**: `tag-confirmed` (a Nebius-owned page, doc or shareholder letter), `tag-reported` (third-party), `tag-inferred` (our reasoning). PANW performance numbers are the same reseller-mirror datasheet figures used on the Lambda site, flagged as needing confirmation.
- The architecture diagram is inline SVG in `architecture.html`, with hard-coded hex colors that match the CSS tokens.

## Key account facts (verified in corpus, Oct 29, 2026)

- **US sites (7 on Nebius's Q2 2026 map plus 1 lease):** Kansas City (Patmos colo, `us-central1`) and Woodbury MN (`us-north1`, B300) are live public regions. Vineland NJ is a DataOne build-to-suit serving Microsoft, with Bloom fuel cells. Independence MO (1.2 GW) and Schuylkill County PA (1.2 GW; 260 MW Oct 2027 → 1 GW+ Nov 2029) are owned. Birmingham AL is owned (~300 MW reported). Oklahoma's partner and MW are undisclosed. An AIB 50 MW southeastern lease was reported in September 2026. Independence, AL and PA are expected online in 2027 (`corpus/ir/shareholder-letter-q1-2026.txt`, `corpus/site/nebius.com__schuylkillcountypa.md`, `docs.nebius.com__overview__regions.md`).
- **Incumbent signal:** a Network Security Engineer posting names "Palo Alto Networks, Check Point" and asks for Panorama, Strata Cloud Manager and FortiManager (`corpus/careers/network-security-engineer-4971845101.md`). The estate is mixed. Network gear in postings: Juniper, Arista, Huawei, Mellanox.
- **Post-mortem:** the us-central1 outage on Sep 3, 2025 was triggered by "new Firewall nodes onboarding" between Nebius's Backbone and DC routing domains (`corpus/blog/nebius.com__blog__posts__incident-post-mortem-analysis-us-central1-service-disruption.md`). Lead every proposal with the insertion design.
- **Tenant network security** is L3/L4 security groups only (GA Feb 2026, 60 rules/group) plus an open-source VM-based IPsec VPN gateway (March 2026). Custom route tables allow appliance or NAT insertion, but traffic within a network can't be steered (`docs.nebius.com__vpc__*`).
- **NICs:** Blackwell hosts have a BlueField-3 400G VPC NIC, and InfiniBand runs 400G/GPU (B200/H200) or 800G/GPU (B300) with per-cluster P-Key isolation on shared fabrics (`docs.nebius.com__compute__virtual-machines__types.md`, `__compute__clusters__gpu.md`).
- **Positioning logic** (same as Lambda): firewalls go north-south only (campus edge PA-7500, PA-5580 per dedicated block, PA-3440 mgmt, PA-415-5G OOB, OT Security for BMS and fuel cells) and never in the IB fabric. AIRS on BlueField is a platform conversation, because Nebius already uses the DPU as its VPC data plane.

## Research tooling

Use WebSearch for press, DCD and local news on sites. Use the SEC 6-K exhibits on sec.gov for filings. The Greenhouse API is `boards-api.greenhouse.io/v1/boards/nebius/jobs` (add `?content=true` for full text in one request). `gh` is not installed.
