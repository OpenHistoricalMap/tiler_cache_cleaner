from concurrent.futures import ThreadPoolExecutor
from tiler_cache_cleaner.utils.files import get_list_expired_tiles
from tiler_cache_cleaner.utils.tiles import generate_patterns_tiles, generate_tile_patterns_bbox
from tiler_cache_cleaner.utils.s3_utils import (
    get_and_delete_existing_tiles,
    delete_objects_with_prefix,
)
from tiler_cache_cleaner.utils.config import Config

MAX_WORKERS = 10


def process_tile(tiles, path_file, zoom_levels_to_delete, tiles_file_name):
    tiles_patterns = generate_patterns_tiles(tiles, zoom_levels_to_delete)
    get_and_delete_existing_tiles(Config.bucket_name, path_file, tiles_patterns, tiles_file_name)


def clean_cache_by_file(expired_file_url, path_file, zoom_levels_to_delete):
    tiles_file_name = expired_file_url.split("/")[-1]
    list_tiles = get_list_expired_tiles(expired_file_url)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for tiles in list_tiles:
            executor.submit(process_tile, tiles, path_file, zoom_levels_to_delete, tiles_file_name)


def clean_cache_by_prefix(prefix_path_file, zoom_levels_to_delete):
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for zoom in zoom_levels_to_delete:
            updated_prefix_path_file = f"{prefix_path_file}/{zoom}"
            executor.submit(
                delete_objects_with_prefix, Config.bucket_name, updated_prefix_path_file
            )


def clean_cache_by_bbox(bbox, zoom_levels_to_delete, prefix_path_file):
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for zoom in zoom_levels_to_delete:
            tiles_patterns = generate_tile_patterns_bbox(bbox, zoom)
            executor.submit(
                get_and_delete_existing_tiles,
                Config.bucket_name,
                prefix_path_file,
                tiles_patterns)
