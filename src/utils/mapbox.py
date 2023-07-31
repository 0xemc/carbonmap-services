import time
import requests

from concurrent.futures import ThreadPoolExecutor

def fetch_tile_image(zoom,x,y,access_token,output_file,scale=2):
    url = f"https://api.mapbox.com/v4/mapbox.satellite/{zoom}/{x}/{y}@{scale}x.jpg90?access_token={access_token}"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_file, 'wb') as out_file:
            out_file.write(response.content)
        print(f"Image successfully downloaded as {output_file}")
    else:
        print(f"Failed to download image, status code: {response.status_code}")
        print(f"Response: {response.text}")

def batch_fetch_tile_image(tiles):
    # Define the maximum number of concurrent requests
    MAX_WORKERS = 10

    # Define the delay between requests (in seconds)
    DELAY = 1

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # For each tile in tiles
        for i, tile in enumerate(tiles):
            # Fetch the tile image
            executor.submit(fetch_tile_image, *tile, API_KEY, f'images/tile_{i}.jpg')
            
            # Delay between requests
            time.sleep(DELAY)

def fetch_static_image(lon1, lat1, lon2, lat2, width, height, scale, access_token, output_file):
    url = f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/%5B{lon1},{lat1},{lon2},{lat2}%5D/{width}x{height}@{scale}x?access_token={access_token}"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_file, 'wb') as out_file:
            out_file.write(response.content)
        print(f"Image successfully downloaded as {output_file}")
    else:
        print(f"Failed to download image, status code: {response.status_code}")
        print(f"Response: {response.text}")