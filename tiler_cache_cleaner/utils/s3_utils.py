import re
from tiler_cache_cleaner.utils.config import Config
from tiler_cache_cleaner.utils.logger import get_logger
from botocore.exceptions import ClientError
import time

logger = get_logger()


def get_and_delete_existing_tiles(
    bucket_name,
    path_file,
    tiles_patterns,
    tiles_file_name="",
    batch_size=1000,
):
    """
    Efficiently check which tile objects exist in S3 and delete them immediately to prevent accumulation.
    """
    s3_client = Config.get_s3_client()
    total_deleted = 0
    total_found = 0
    tile_prefixes = set()
    # Prepare tile prefixes
    for tile in tiles_patterns:
        match = re.match(r"(\d+)/(\d+)", tile)
        if match:
            zoom, x_prefix = match.groups()
            prefix = f"{path_file}/{zoom}/{x_prefix}"
            tile_prefixes.add(prefix)

    start_time = time.time()
    total_patterns = len(tile_prefixes)
    processed_patterns = 0

    try:
        for prefix in tile_prefixes:
            paginator = s3_client.get_paginator("list_objects_v2")
            response_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

            objects_to_delete = []
            found_this_prefix = 0

            for page in response_iterator:
                contents = page.get("Contents", [])
                total_found += len(contents)
                found_this_prefix += len(contents)

                for obj in contents:
                    obj_key = obj["Key"]
                    objects_to_delete.append({"Key": obj_key})

                    if len(objects_to_delete) >= batch_size:
                        s3_client.delete_objects(
                            Bucket=bucket_name, Delete={"Objects": objects_to_delete}
                        )
                        total_deleted += len(objects_to_delete)
                        logger.info(
                            f"[{processed_patterns + 1}/{total_patterns}] Deleted {len(objects_to_delete)} tiles under {prefix}*"
                        )
                        objects_to_delete = []

            if objects_to_delete:
                s3_client.delete_objects(Bucket=bucket_name, Delete={"Objects": objects_to_delete})
                total_deleted += len(objects_to_delete)

            processed_patterns += 1
            logger.info(
                f"[{processed_patterns}/{total_patterns}] Deleted {found_this_prefix} objects under prefix {prefix}"
            )

    except ClientError as e:
        logger.error(f"S3 ClientError while fetching or deleting tiles: {e}")
        raise
    except Exception as e:
        logger.error(f"Error while fetching or deleting tiles from S3: {e}")
        raise

    elapsed_time = time.time() - start_time
    logger.info(
        f"{tiles_file_name}-> S3 cleanup completed in {elapsed_time:.2f} seconds, Total tiles found: {total_found}, Total deleted tiles: {total_deleted}"
    )

    return total_deleted


def delete_objects_with_prefix(bucket_name, prefix):
    """Delete all objects in the S3 bucket with the specified prefix."""
    logger.info(
        f"Starting deletion of all objects in bucket '{bucket_name}' with prefix '{prefix}'"
    )
    s3_client = Config.get_s3_client()

    paginator = s3_client.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    deleted = 0
    page_count = 0

    for page in page_iterator:
        page_count += 1
        objects = page.get("Contents", [])
        if not objects:
            logger.info(
                f"No objects found in page {page_count} for prefix '{prefix}' in bucket '{bucket_name}'"
            )
            continue

        keys = [{"Key": obj["Key"]} for obj in objects]
        response = s3_client.delete_objects(Bucket=bucket_name, Delete={"Objects": keys})

        deleted_count = len(response.get("Deleted", []))
        deleted += deleted_count

    logger.info(
        f"Deletion complete for prefix '{prefix}' in bucket '{bucket_name}'. Total objects deleted: {deleted}"
    )
