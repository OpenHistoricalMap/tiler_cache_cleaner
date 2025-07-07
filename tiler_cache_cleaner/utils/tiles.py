import re
from tiler_cache_cleaner.utils.logger import get_logger
import mercantile

logger = get_logger()


def generate_patterns_tiles(tiles, zoom_levels):
    """
    Generate zoom/x_prefix patterns from input tiles for the specified zoom levels.

    Includes:
    - The current tile's zoom (if in zoom_levels)
    - Parent tiles (if their zoom is in zoom_levels)
    - Child tiles down to the max zoom in zoom_levels

    Args:
        tiles (list): List of tile strings in "z/x/y" format.
        zoom_levels (list or int): Target zoom levels for pattern generation.

    Returns:
        list: Sorted list of unique zoom/x prefix strings.
    """
    if isinstance(zoom_levels, int):
        zoom_levels = [zoom_levels]
    elif not zoom_levels:
        logger.warning("zoom_levels is empty, returning no patterns.")
        return []

    zoom_levels = sorted(set(zoom_levels))
    patterns = set()

    def add_pattern(z, x):
        if z not in zoom_levels:
            return
        x_str = str(x)
        if len(x_str) <= 2:
            prefix = f"{z}/{x_str}"
        elif len(x_str) == 3:
            prefix = f"{z}/{x_str[:-1]}"
        else:
            prefix = f"{z}/{x_str[:-2]}"
        patterns.add(prefix)

    for tile in tiles:
        match = re.match(r"(\d+)/(\d+)/(\d+)", tile)
        if not match:
            logger.warning(f"Skipping invalid tile format: {tile}")
            continue

        z, x, y = map(int, match.groups())

        # Add current tile
        add_pattern(z, x)

        # Add parent tiles (upward) if in zoom_levels
        px = x
        for parent_zoom in range(z - 1, min(zoom_levels) - 1, -1):
            px //= 2
            add_pattern(parent_zoom, px)

        # Add child tiles (downward) if in zoom_levels
        for child_zoom in range(z + 1, max(zoom_levels) + 1):
            factor = 2 ** (child_zoom - z)
            for dx in range(factor):
                add_pattern(child_zoom, x * factor + dx)

    sorted_patterns = sorted(patterns)
    logger.info(
        f"Generated {len(sorted_patterns)} tile patterns from {len(tiles)} input tiles at zooms {zoom_levels}."
    )
    return sorted_patterns


def generate_tile_patterns_bbox(bbox, zoom):
    """
    Generate minimal set of unique tile prefixes z/x_prefix based on tile.x only.
    Optimized to avoid iterating over full tile list (x/y).
    """
    prefixes = set()
    minx, miny, maxx, maxy = bbox
    tile_ul = mercantile.tile(minx, maxy, zoom)  # upper-left corner
    tile_lr = mercantile.tile(maxx, miny, zoom)  # lower-right corner

    min_x, max_x = tile_ul.x, tile_lr.x

    logger.info(f"Zoom {zoom}: X range {min_x} to {max_x}")

    for x in range(min_x, max_x + 1):
        x_str = str(x)
        if len(x_str) <= 2:
            x_prefix = x_str
        elif len(x_str) == 3:
            x_prefix = x_str[:-1]
        else:
            x_prefix = x_str[:-2]

        prefixes.add(f"{zoom}/{x_prefix}")

    logger.info(f"Total unique prefixes: {len(prefixes)}")
    return sorted(prefixes)
