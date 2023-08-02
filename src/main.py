import os
import concurrent.futures
import pandas as pd
from tree_detect import predict_tile_img
from shapely.geometry import Polygon
from constants import MT_WELLINGTON_BOUNDING_BOX, API_KEY
from utils.geo import tiles_in_polygon, point_in_tile_to_latlon
from utils.mapbox import batch_fetch_tile_image

# Build our Shapely polygon from our BOUNDING_BOX
polygon = Polygon(MT_WELLINGTON_BOUNDING_BOX)

# Find all the tiles within our chosen area
tiles = tiles_in_polygon(polygon, 18)[:3]

# Fetch missing images
batch_fetch_tile_image(tiles, 18, API_KEY)

# Get a list of all files in the 'images' directory
image_files = os.listdir("images")

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
