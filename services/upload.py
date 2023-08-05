import os

from shapely.geometry import Polygon
from typing import TypedDict, List
from datetime import datetime

from services.shared.constants import API_KEY
from services.shared.utils.geo import tiles_in_polygon
from services.shared.utils.mapbox import batch_fetch_tile_image
from services.shared.utils.supabase import batch_upload_file, FileDict


def upload(bucket: str, files: list[str]):
    destination_dir = todays_date()

    # Create a list of FileDict from the above files
    file_dicts = [
        FileDict(source=file, destination=extract_filename(file)) for file in files
    ]

    # Store the files
    batch_upload_file(bucket, destination_dir, file_dicts)


def extract_filename(file_path: str) -> str:
    return os.path.basename(file_path)


def todays_date() -> str:
    return datetime.now().strftime("%d-%m-%Y")
