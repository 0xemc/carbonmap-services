import os
import matplotlib.pyplot as plt
import pandas as pd
from deepforest import main
from utils.geo import point_in_tile_to_latlon

def predict(image_path, plot=False):
    model = main.deepforest()
    model.use_release()
    return model.predict_image(path=image_path, return_plot=plot)

def show(data):
    plt.imshow(data[:,:,::-1])
    plt.show() 

def process_row(row):
    lat, lon = point_in_tile_to_latlon(238316, 165684, row['x_norm'], row['y_norm'], 18)
    return pd.Series([lat, lon])

# This function relies on the naming format of tile_x_y_zoom.jpg in order to get the tile details
def predict_tile_img(image_file):
    if image_file.endswith('.jpg'):
        file_path = os.path.join('images', image_file)
        
        import re
        
        # Extract the tile x and y from the image_file path
        match = re.search(r'tile_(\d+)_(\d+)_\d+.jpg', image_file)

        if not match:
            raise ValueError("File format did not match as expected. Expected format: 'tile_x_y_zoom.jpg'")

        tile_x, tile_y = map(int, match.groups())

        # Count the trees!
        result = predict(file_path)
        
        # Calculate the center points
        result['x_center'] = (result['xmin'] + result['xmax']) / 2 
        result['y_center'] = (result['ymin'] + result['ymax']) / 2 
        result['x_norm'] = result['x_center'] / 512
        result['y_norm'] = result['y_center'] / 512

      # Define process_row as a lambda function
        process_row = lambda row: pd.Series(point_in_tile_to_latlon(tile_x, tile_y, row['x_norm'], row['y_norm'], 18))

        result[['lat', 'lon']] = result.apply(process_row, axis=1)
        return result[['lat','lon']]