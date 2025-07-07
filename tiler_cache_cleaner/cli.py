"""

E.g
python -m tiler-cache-cleaner clean_file --expired-file-url=https://s3.us-east-1.amazonaws.com/planet-staging.openhistoricalmap.org/imposm/imposm3_expire_dir/20241210/114154.074.tiles --path-file "mnt/data/osm" --zoom-levels "1,2,3,4,5"

"""

import typer
from tiler_cache_cleaner.cleaner import (
    clean_cache_by_file,
    clean_cache_by_prefix,
    clean_cache_by_bbox,
)

app = typer.Typer()


@app.command("clean_by_file")
def clean_by_file(
    expired_file_url: str = typer.Option(
        "https://s3.us-east-1.amazonaws.com/planet-staging.openhistoricalmap.org/imposm/imposm3_expire_dir/20241210/114154.074.tiles",
        "--expired-file-url",
        help="Public URL to expired tiles file",
    ),
    path_file: str = typer.Option(
        "mnt/data/osm", "--prefix-path-file", help="Path prefix to cached tiles"
    ),
    zoom_levels: str = typer.Option(
        "8,9,10,11,12,13,14,15,16,17,18,19,20", "--zoom-levels", help="Comma-separated zoom levels"
    ),
):
    zoom_levels_to_delete = [int(z) for z in zoom_levels.split(",")]
    clean_cache_by_file(expired_file_url, path_file, zoom_levels_to_delete)


@app.command("clean_by_prefix")
def clean_by_prefix(
    prefix_path_file: str = typer.Option(
        "mnt/data/osm", "--prefix-path-file", help="Path prefix to cached tiles"
    ),
    zoom_levels: str = typer.Option(
        "8,9,10,11,12,13,14,15,16,17,18,19,20", "--zoom-levels", help="Comma-separated zoom levels"
    ),
):
    """
    Delete all cached tiles from a specific path prefix and zoom levels. for OHM, could be "mnt/data/osm,mnt/data/osm_land or mnt/data/ne "

    This command removes all raster/vector tiles stored under the given prefix_path_file
    for the specified zoom levels. Useful for cleaning up outdated or unused tile cache.
    """
    zoom_levels_to_delete = [int(z) for z in zoom_levels.split(",")]
    clean_cache_by_prefix(prefix_path_file, zoom_levels_to_delete)


@app.command("clean_by_bbox")
def clean_bbox(
    bbox: str = typer.Option(
        ..., "--bbox", help="Bounding box to clean tiles (format: minLon,minLat,maxLon,maxLat)"
    ),
    zoom_levels: str = typer.Option(
        "8,9,10,11,12,13,14,15,16,17,18,19,20", "--zoom-levels", help="Comma-separated zoom levels"
    ),
    prefix_path_file: str = typer.Option(
        "mnt/data/osm", "--prefix-path-file", help="Path prefix to cached tiles"
    ),
):
    """
    Clean cached tiles that fall within the given bounding box and zoom levels.
    """
    minx, miny, maxx, maxy = [float(v.strip()) for v in bbox.split(",")]
    bbox = [minx, miny, maxx, maxy]
    zoom_levels_to_delete = [int(z) for z in zoom_levels.split(",")]
    clean_cache_by_bbox(bbox, zoom_levels_to_delete, prefix_path_file)
