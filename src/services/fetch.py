import os

from shapely.geometry import Polygon
from typing import TypedDict, List
from datetime import datetime

from shared.constants import API_KEY
from shared.utils.geo import tiles_in_polygon
from shared.utils.mapbox import batch_fetch_tile_image
from shared.utils.supabase import batch_upload_file, FileDict


# ------ Fetch Tile Images ------ #
def fetch(geo_shape: List[List[float]], resolution=18, limit=100):
    # Build our Shapely polygon from our BOUNDING_BOX
    polygon = Polygon(geo_shape)

    # Find all the tiles within our chosen area
    tiles = tiles_in_polygon(polygon, resolution)[:limit]

    shouldContinue = input(
        f"You are about to fetch {len(tiles)} images. Continue? (Y/n)"
    )

    if shouldContinue == "n":
        exit
    # # Fetch missing images
    files = batch_fetch_tile_image(tiles, resolution, API_KEY)

    return files
