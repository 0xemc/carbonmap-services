import os

from shapely.geometry import Polygon
from typing import TypedDict, List
from datetime import datetime

from services.shared.constants import API_KEY
from services.shared.utils.geo import tiles_in_polygon
from services.shared.utils.mapbox import batch_fetch_tile_image
from services.shared.utils.supabase import batch_store, FileDict


class BoundingBox(TypedDict):
    name: str
    shape: List[List[float]]


# ------ Fetch Tile Images ------ #
def fetch(bounding_box: BoundingBox, resolution=18, limit=100):
    # Build our Shapely polygon from our BOUNDING_BOX
    polygon = Polygon(bounding_box["shape"])

    # Find all the tiles within our chosen area
    tiles = tiles_in_polygon(polygon, resolution)[:limit]

    # Fetch missing images
    files = batch_fetch_tile_image(tiles, resolution, API_KEY)

    destination_dir = todays_date()

    # Create a list of FileDict from the above files
    file_dicts = [
        FileDict(source=file, destination=extract_filename(file)) for file in files
    ]

    # Store the files
    batch_store(bounding_box["name"], destination_dir, file_dicts)


def extract_filename(file_path: str) -> str:
    return os.path.basename(file_path)


def todays_date() -> str:
    return datetime.now().strftime("%d-%m-%Y")
