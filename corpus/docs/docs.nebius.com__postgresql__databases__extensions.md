# Extensions in Managed Service for PostgreSQL®

Source: https://docs.nebius.com/postgresql/databases/extensions

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nebius.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Extensions in Managed Service for PostgreSQL®

Managed Service for PostgreSQL clusters are created with pre-installed PostgreSQL extensions. You can enable any of these extensions for your databases, but you cannot install any other extensions. See the full list of available extensions [below](#available-extensions), or you can [request the list](#how-to-request-the-list-of-installed-extensions).

## How to enable an extension for a database

To enable an extension for a database, execute the [CREATE EXTENSION](https://www.postgresql.org/docs/16/sql-createextension.html) statement:

```sql theme={null}
CREATE EXTENSION <extension_name>;
```

This command does not affect other databases in the cluster. To use an extension in other databases, execute `CREATE EXTENSION` in each one as needed.

### Example: pgvector extension

To get started with the [pgvector](https://github.com/pgvector/pgvector) open-source extension, which provides vector operations, follow these steps:

1. Add the extension:

   ```sql theme={null}
   CREATE EXTENSION vector;
   ```

2. Create a table with a vector column:

   ```sql theme={null}
   CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
   ```

3. Insert some vectors into the new table:

   ```sql theme={null}
   INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');
   ```

4. Get the contents of the table sorted by how close each value is to a given vector (that is, sorted by [Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance)):

   ```sql theme={null}
   SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;
   ```

## How to request the list of installed extensions

To get the list of extensions available on your cluster, execute the following statement:

```sql theme={null}
SELECT * FROM pg_available_extensions;
```

To look for a particular extension, execute the following statement:

```sql theme={null}
SELECT * FROM pg_available_extensions WHERE name LIKE '<extension_name>';
```

## Available extensions

| Extension | Version | Description |
| - | - | - |
| [adminpack](https://www.postgresql.org/docs/16/adminpack.html) | 2.1 | Provides support functions for administration and management tools. |
| [amcheck](https://www.postgresql.org/docs/16/amcheck.html) | 1.3 | Provides functions that verify the logical consistency of the structure of relations. |
| [autoinc](https://www.postgresql.org/docs/16/contrib-spi.html#CONTRIB-SPI-AUTOINC) | 1.0 | Provides functions that autoincrement fields. |
| [bloom](https://www.postgresql.org/docs/16/bloom.html) | 1.0 | Implements an index access method based on Bloom filters. |
| [btree\_gin](https://www.postgresql.org/docs/16/btree-gin.html) | 1.3 | Supports indexing common data types by using GIN (generalized inverted index). |
| [btree\_gist](https://www.postgresql.org/docs/16/btree-gist.html) | 1.7 | Supports indexing common data types by using GiST (generalized search tree). |
| [citext](https://www.postgresql.org/docs/16/citext.html) | 1.6 | Defines a data type for case-insensitive character strings. |
| [cube](https://www.postgresql.org/docs/16/cube.html) | 1.5 | Defines a data type for multidimensional cubes. |
| [dblink](https://www.postgresql.org/docs/16/dblink.html) | 1.2 | Allows connections to other PostgreSQL databases from within a database. |
| [dict\_int](https://www.postgresql.org/docs/16/dict-int.html) | 1.0 | Defines a text search dictionary template for processing integers. |
| [dict\_xsyn](https://www.postgresql.org/docs/16/dict-xsyn.html) | 1.0 | Defines a text search dictionary template for extended synonym processing. |
| [earthdistance](https://www.postgresql.org/docs/16/earthdistance.html) | 1.1 | Calculates great-circle distances on the surface of the Earth. |
| [file\_fdw](https://www.postgresql.org/docs/16/file-fdw.html) | 1.0 | Provides a foreign-data wrapper to access data files in the server's file system. |
| [fuzzystrmatch](https://www.postgresql.org/docs/16/fuzzystrmatch.html) | 1.2 | Provides functions that determine similarities and distances between strings. |
| [hstore](https://www.postgresql.org/docs/16/hstore.html) | 1.8 | Defines a data type that stores sets of key-value pairs. |
| [insert\_username](https://www.postgresql.org/docs/16/contrib-spi.html#CONTRIB-SPI-INSERT-USERNAME) | 1.0 | Provides functions that track which user changed a table. |
| [intagg](https://www.postgresql.org/docs/16/intagg.html) | 1.1 | Defines an integer aggregator and enumerator. The module is provided for compatibility and is obsolete. |
| [intarray](https://www.postgresql.org/docs/16/intarray.html) | 1.5 | Provides functions and operators that manipulate null-free arrays of integers. |
| [isn](https://www.postgresql.org/docs/16/isn.html) | 1.2 | Defines data types for international product numbering standards. |
| [lo](https://www.postgresql.org/docs/16/lo.html) | 1.1 | Supports large object management. |
| [ltree](https://www.postgresql.org/docs/16/ltree.html) | 1.2 | Defines a data type for hierarchical tree-like structures. |
| [moddatetime](https://www.postgresql.org/docs/16/contrib-spi.html#CONTRIB-SPI-MODDATETIME) | 1.0 | Provides functions that track the last modification time of records. |
| [old\_snapshot](https://www.postgresql.org/docs/16/oldsnapshot.html) | 1.0 | Provides utilities that manage old snapshot thresholds. |
| [pageinspect](https://www.postgresql.org/docs/16/pageinspect.html) | 1.12 | Provides functions that inspect the contents of database pages at a low level. |
| [pg\_buffercache](https://www.postgresql.org/docs/16/pgbuffercache.html) | 1.4 | Provides a means of examining the shared buffer cache. |
| [pg\_freespacemap](https://www.postgresql.org/docs/16/pgfreespacemap.html) | 1.2 | Provides a means of examining the free space map. |
| [pg\_prewarm](https://www.postgresql.org/docs/16/pgprewarm.html) | 1.2 | Loads relation data into the buffer cache. |
| [pg\_repack](https://github.com/reorg/pg_repack) | 1.5.2 | Reorganizes tables and indexes with minimal locks. See [how to run pg\_repack](#how-to-run-pg_repack) on a Managed Service for PostgreSQL cluster. |
| [pg\_stat\_statements](https://www.postgresql.org/docs/16/pgstatstatements.html) | 1.10 | Tracks planning and execution statistics for SQL statements. |
| [pg\_surgery](https://www.postgresql.org/docs/16/pgsurgery.html) | 1.0 | Provides functions that perform "surgery" on damaged relations. |
| [pg\_trgm](https://www.postgresql.org/docs/16/pgtrgm.html) | 1.6 | Measures text similarity and supports index searching based on trigram matching. |
| [pg\_visibility](https://www.postgresql.org/docs/16/pgvisibility.html) | 1.2 | Provides a means of examining the visibility map and page-level visibility information. |
| [pg\_walinspect](https://www.postgresql.org/docs/16/pgwalinspect.html) | 1.1 | Provides functions that inspect the PostgreSQL write-ahead log. |
| [pgaudit](https://github.com/pgaudit/pgaudit) | 16.0 | Provides detailed session and object audit logging via the standard PostgreSQL logging facility. |
| [pgcrypto](https://www.postgresql.org/docs/16/pgcrypto.html) | 1.3 | Provides cryptographic functions. |
| [pgrowlocks](https://www.postgresql.org/docs/16/pgrowlocks.html) | 1.2 | Displays row-level locking information. |
| [pgstattuple](https://www.postgresql.org/docs/16/pgstattuple.html) | 1.5 | Provides functions to obtain tuple-level statistics. |
| [plpgsql](https://www.postgresql.org/docs/16/plpgsql.html) | 1.0 | PL/pgSQL procedural language for PostgreSQL. |
| [postgres\_fdw](https://www.postgresql.org/docs/16/postgres-fdw.html) | 1.1 | Provides a foreign-data wrapper for connecting to external PostgreSQL servers. |
| [refint](https://www.postgresql.org/docs/16/contrib-spi.html#CONTRIB-SPI-REFINT) | 1.0 | Provides functions for referential integrity. The module is provided for compatibility and is obsolete. |
| [rum](https://github.com/postgrespro/rum) | 1.3 | Provides an access method for working with RUM indexes. |
| [seg](https://www.postgresql.org/docs/16/seg.html) | 1.4 | Defines a data type that represents line segments or floating-point intervals. |
| [sslinfo](https://www.postgresql.org/docs/16/sslinfo.html) | 1.2 | Provides information about SSL certificates. |
| [tablefunc](https://www.postgresql.org/docs/16/tablefunc.html) | 1.0 | Implements functions that manipulate whole tables, including `crosstab` operations. |
| [tcn](https://www.postgresql.org/docs/16/tcn.html) | 1.0 | Provides a trigger function that notifies listeners of changes. |
| [tsm\_system\_rows](https://www.postgresql.org/docs/16/tsm-system-rows.html) | 1.0 | Provides a `TABLESAMPLE` method that reads no more than the given number of rows. |
| [tsm\_system\_time](https://www.postgresql.org/docs/16/tsm-system-time.html) | 1.0 | Provides a `TABLESAMPLE` method that spends no longer than the given time to read the table. |
| [unaccent](https://www.postgresql.org/docs/16/unaccent.html) | 1.1 | Defines a text search dictionary that removes diacritics. |
| [uuid-ossp](https://www.postgresql.org/docs/16/uuid-ossp.html) | 1.1 | Generates universally unique identifiers (UUIDs). |
| [vector (pgvector)](https://github.com/pgvector/pgvector) | 0.8 | Defines a vector data type with `ivfflat` and `hnsw` access methods for vector searches. |
| [xml2](https://www.postgresql.org/docs/16/xml2.html) | 1.1 | Provides functions for XPath querying and XSLT processing. |

## How to run pg\_repack

Managed Service for PostgreSQL clusters do not provide superuser access. Therefore, run the [pg\_repack](https://github.com/reorg/pg_repack) extension only on the tables that you own and include the `--no-superuser-check` parameter. For example:

```bash theme={null}
pg_repack \
  --host=<cluster_endpoint> \
  --dbname=<DB_name> \
  --username=<username> \
  --table=<table_name> \
  --jobs=4 \
  --wait-timeout=600 \
  --no-superuser-check
```

In this command, specify the same parameters that you use for [connecting to the cluster](https://docs.nebius.com/postgresql/databases/connect.md). Ensure that `<username>` owns `<table_name>`.

***

*Postgres, PostgreSQL and the Slonik Logo are trademarks or registered trademarks of the PostgreSQL Community Association of Canada, and used with their permission.*
