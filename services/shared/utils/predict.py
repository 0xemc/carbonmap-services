import os
import re
import matplotlib.pyplot as plt
import pandas as pd
from deepforest import main
from services.shared.utils.geo import point_in_tile_to_latlon
from geoalchemy2 import WKTElement


def predict(image_path, plot=False):
    model = main.deepforest()
    model.use_release(check_release=False)
    return model.predict_image(path=image_path, return_plot=plot)


def show(data):
    plt.imshow(data[:, :, ::-1])
    plt.show()


def process_row(row):
    lat, lon = point_in_tile_to_latlon(238316, 165684, row["x_norm"], row["y_norm"], 18)
    return pd.Series([lat, lon])


# This function relies on the naming format of tile_x_y_zoom.jpg in order to get the tile details
def predict_tile_img(image_file):
    if image_file.endswith(".jpg"):
        # Extract the tile x and y from the image_file path
        match = re.search(r".*\/(\d+)_(\d+)_(\d+).jpg", image_file)

        if not match:
            raise ValueError(
                "File format did not match as expected. Expected format: 'tile_x_y_zoom.jpg'",
                image_file,
            )

        tile_x, tile_y, zoom = map(int, match.groups())

        # Count the trees!
        result = predict(image_file)

        # Calculate the center points
        result["x_center"] = (result["xmin"] + result["xmax"]) / 2
        result["y_center"] = (result["ymin"] + result["ymax"]) / 2
        result["x_norm"] = result["x_center"] / 512
        result["y_norm"] = result["y_center"] / 512

        # Define process_row as a lambda function
        add_lat_lng = lambda row: pd.Series(
            point_in_tile_to_latlon(tile_x, tile_y, row["x_norm"], row["y_norm"], zoom)
        )

        # Convert lat and lon to a Point geometry (this assumes lon and lat are in degrees)
        add_point_geometry = lambda row: WKTElement(
            f"POINT({row.lon} {row.lat})", srid=4326
        )

        result[["lat", "lon"]] = result.apply(add_lat_lng, axis=1)
        result["geom"] = result.apply(add_point_geometry, axis=1)

        return result[["geom", "image_path", "score", "lat", "lon"]]
