"""

E.g
python -m tiler-cache-cleaner clean_file --expired-file-url=https://s3.us-east-1.amazonaws.com/planet-staging.openhistoricalmap.org/imposm/imposm3_expire_dir/20241210/114154.074.tiles --path-file "/mnt/data/osm" --zoom-levels "1,2,3,4,5"

"""

import typer
from tiler_cache_cleaner.cleaner import clean_cache_by_file

app = typer.Typer()


@app.command("clean_file")  # Registra subcomando 'clean'
def clean_file(
    expired_file_url: str = typer.Option(
        "https://s3.us-east-1.amazonaws.com/planet-staging.openhistoricalmap.org/imposm/imposm3_expire_dir/20241210/114154.074.tiles",
        "--expired-file-url",
        help="Public URL to expired tiles file",
    ),
    path_file: str = typer.Option(
        "/mnt/data/osm", "--path-file", help="Path prefix to cached tiles"
    ),
    zoom_levels: str = typer.Option(
        "1,2,3,4,5", "--zoom-levels", help="Comma-separated zoom levels"
    ),
):
    zoom_levels_to_delete = [int(z) for z in zoom_levels.split(",")]
    clean_cache_by_file(expired_file_url, path_file, zoom_levels_to_delete)


@app.command("clean_bbox")  # Registra subcomando 'clean'
def clean_bbox(
    path_file: str = typer.Option(
        "/mnt/data/osm", "--path-file", help="Path prefix to cached tiles"
    ),
    zoom_levels: str = typer.Option(
        "1,2,3,4,5", "--zoom-levels", help="Comma-separated zoom levels"
    ),
):
    print("==========")
