import requests
from tiler_cache_cleaner.utils.logger import get_logger

logger = get_logger()


def get_list_expired_tiles(url):
    """
    Fetches a list of expired tiles from a public URL,
    ensures uniqueness, and returns them in chunks of 1000.

    Args:
        url (str): Public URL pointing to the expired tiles file.

    Returns:
        list[list[str]]: A list of chunks, each containing up to 1000 unique tile paths.
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError(f"Invalid URL format: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()

        file_content = response.text.strip()

        if not file_content:
            logger.warning("The file is empty. No expired tiles found.")
            return []

        unique_tiles = list(set(file_content.splitlines()))
        unique_tiles.sort()
        logger.info(f"Number of unique expired tiles: {len(unique_tiles)}")

        # Split into chunks of 1000
        chunk_size = 1000
        chunks = [unique_tiles[i : i + chunk_size] for i in range(0, len(unique_tiles), chunk_size)]
        logger.info(f"Split into {len(chunks)} chunks of max {chunk_size} each")
        return chunks

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Error reading file from URL: {e}")
        raise
