import pandas as pd
from shared.constants import (
    API_KEY,
    NEW_NORFOLK_BOUNDING_BOX,
)
from shapely.geometry import Polygon
from shared.utils.geo import tiles_in_polygon
from shared.utils.mapbox import batch_fetch_tile_image


# ------ Fetch Tile Images ------ #
def fetch(bounding_box: list[list[float]], resolution=18, limit=3):
    # Build our Shapely polygon from our BOUNDING_BOX
    # polygon = Polygon(bounding_box)

    # Find all the tiles within our chosen area
    # tiles = tiles_in_polygon(polygon, resolution)[:limit]

    # Fetch missing images
    # batch_fetch_tile_image(tiles, resolution, API_KEY)

    return "Success"
