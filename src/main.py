import pandas as pd
from tree_detect import predict
from shapely.geometry import Polygon
from constants import mt_wellington_bounding_box
from utils.geo import tiles_in_polygon
import os

# Mapbox API Key
API_KEY = os.environ.get('API_MAPBOX_KEY')

# Yaizu Court Bounding Box
BOUNDING_BOX = (147.2777, -42.8645, 147.279, -42.8639)

YAIZU_TILE = (18, 238316, 165684)

# Fetch the satellite image
# fetch_tile_image(*BOUNDING_BOX, 1200, 800, 2, API_KEY, 'images/test.jpg')
# fetch_tile_image(*YAIZU_TILE, API_KEY, 'images/test.jpg')

polygon = Polygon(mt_wellington_bounding_box)

tiles = tiles_in_polygon(polygon, 18)

print(len(tiles))

# Count the trees!
# result = predict('images/test.jpg')

# # Calculate the center points
# result['x_center'] = (result['xmin'] + result['xmax']) / 2 
# result['y_center'] = (result['ymin'] + result['ymax']) / 2 
# result['x_norm'] = result['x_center'] / 512
# result['y_norm'] = result['y_center'] / 512


# def process_row(row):
#     lat, lon = point_in_tile_to_latlon(238316, 165684, row['x_norm'], row['y_norm'], 18)
#     return pd.Series([lat, lon])

# result[['lat', 'lon']] = result.apply(process_row, axis=1)

# print(result[['lat','lon']])


