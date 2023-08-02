import os
import concurrent.futures
import pandas as pd
from tree_detect import predict_tile_img
from shapely.geometry import Polygon
from constants import MT_WELLINGTON_BOUNDING_BOX, API_KEY, POSTGRES_URL
from utils.geo import tiles_in_polygon
from utils.mapbox import batch_fetch_tile_image
from sqlalchemy import create_engine
from geoalchemy2 import Geometry

# ------ Fetch Tile Images ------ #
# Build our Shapely polygon from our BOUNDING_BOX
polygon = Polygon(MT_WELLINGTON_BOUNDING_BOX)

# Find all the tiles within our chosen area
tiles = tiles_in_polygon(polygon, 18)[:3]

# Fetch missing images
batch_fetch_tile_image(tiles, 18, API_KEY)

# Get a list of all files in the 'images' directory
image_files = os.listdir("images")


# -------  Find the Trees  -------- #
# Create a ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Use list comprehension to create a list of futures
    futures = [
        executor.submit(predict_tile_img, image_file) for image_file in image_files
    ]

    # Collate the results into a single array
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

    merged_results = pd.concat(results, ignore_index=True)

print(merged_results)

#  ----- Write to DB ------
engine = create_engine(POSTGRES_URL)

# Write DataFrame to PostGIS table "trees"
merged_results.to_sql(
    "trees",
    engine,
    if_exists="append",
    index=False,
    dtype={"geom": Geometry("POINT", srid=4326)},
)
