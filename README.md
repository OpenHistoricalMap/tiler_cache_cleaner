# Tiler Cache Cleaner

This Python module enables efficient deletion of tile cache files stored in AWS S3, using batch deletions of up to 1,000 objects per request. This script has already been tested in our production workflows and is now being migrated into its own standalone module for improved performance and flexibility.

Why?

Cache cleaning in Tegola can be slow, especially when dealing with large areas like entire countries or continents. In such cases, the process may take several hours, which is highly inefficient. https://github.com/go-spatial/tegola/issues/722

Background

The original version of this script was written under the [ohm-deploy/images/tiler-cache](https://github.com/OpenHistoricalMap/ohm-deploy/blob/d31fb9cf248b778520029fb2f89514fc60323586/images/tiler-cache/utils/s3_utils.py) directory. It used AWS S3’s batch deletion capability to remove up to 1,000 objects per request—significantly speeding up the cache cleanup process.

About This Module

This new Python module improves upon the original by offering:
	•	Cleaner project structure
	•	Improved performance
	•	Unit testing for better reliability
	•	CLI support using typer


While this module was initially considered to be directly attached to Tegola, our current workflows in OpenHistoricalMap rely on AWS SQS for managing cache invalidation. To avoid coupling to a specific tile generator and allow more flexibility, we opted to keep this tool as an independent module.

# CLI

- Remove all tiles under a given prefix for specific zoom levels e.g

```sh
tiler-cache-cleaner clean_by_prefix \
    --prefix-path-file="mnt/data/osm" \
    --zoom-levels="0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20"

```

- Remove tiles listed in an Imposm expired file (format: z/x/y) for a specific prefix and zoom levels. e.g

```sh
tiler-cache-cleaner clean_by_file \
    --expired-file-url="https://s3.us-east-1.amazonaws.com/planet-staging.openhistoricalmap.org/imposm/imposm3_expire_dir/20241210/114154.074.tiles" \
    --prefix-path-file="mnt/data/osm" \
    --zoom-levels="1,2,3,4,5"
```


- Remove all tiles within a bounding box for a specific prefix and zoom levels. e.g

```sh
tiler-cache-cleaner clean_by_bbox \
    --prefix-path-file="mnt/data/osm" \
    --zoom-levels="11,12,13,14,15,16" \
    --bbox="-74.259875,-13.200409,-74.190009,-13.119005"
```


<!-- python -m tiler_cache_cleaner clean_by_bbox -->