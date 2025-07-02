from concurrent.futures import ThreadPoolExecutor
from tiler_cache_cleaner.utils.files import get_list_expired_tiles
from tiler_cache_cleaner.utils.tiles import (
    generate_patterns_children_tiles,
    get_and_delete_existing_tiles,
)
from tiler_cache_cleaner.utils.config import Config

MAX_WORKERS = 10


def process_tile(tile, path_file, zoom_levels_to_delete):
    tiles_patterns = generate_patterns_children_tiles(tile, zoom_levels_to_delete)
    get_and_delete_existing_tiles(Config.bucket_name, path_file, tiles_patterns)


def clean_cache_by_file(expired_file_url, path_file, zoom_levels_to_delete):
    list_tiles = get_list_expired_tiles(expired_file_url)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for tile in list_tiles:
            executor.submit(process_tile, tile, path_file, zoom_levels_to_delete)


# python -m tiler_cache_cleaner clean "https://s3.us-east-1.amazonaws.com/planet-staging.openhistoricalmap.org/imposm/imposm3_expire_dir/20241210/114154.074.tiles" --path-file "/mnt/data/osm" --zoom-levels "1,2,3,4,5"
