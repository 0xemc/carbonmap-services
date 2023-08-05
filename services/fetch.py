from services.shared.constants import (
    API_KEY,
)
from services.shared.utils.geo import tiles_in_polygon
from services.shared.utils.mapbox import batch_fetch_tile_image
from shapely.geometry import Polygon


class BoundingBox:
    name: str
    shape: list[list[float]]


# ------ Fetch Tile Images ------ #
def fetch(bounding_box: BoundingBox, resolution=18, limit=3):
    # Build our Shapely polygon from our BOUNDING_BOX
    polygon = Polygon(bounding_box.shape)

    # Find all the tiles within our chosen area
    tiles = tiles_in_polygon(polygon, resolution)[:limit]

    # Fetch missing images
    files = batch_fetch_tile_image(tiles, resolution, API_KEY)

    # Create a list of FileDict from the above files
    file_dicts = [{"source": file, "destination": file["path"]} for file in files]

    # # Store the files
    # batch_store(bounding_box.name, file_dicts)

    return files
