import math
from shapely.geometry import box

def point_in_tile_to_latlon(tile_x, tile_y, point_x, point_y, zoom):
    n = 2.0 ** zoom
    lon_deg = (tile_x + point_x) / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * (tile_y + point_y) / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

def latlon_to_tile(lat, lon, zoom):
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    # Add a small offset to lat if it's an odd multiple of 90 degrees
    if lat % 180 == 90:
        lat += 1e-10
    ytile = int((1.0 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

# Note: This logic grabs the tiles that intersect our polygon. This means that the only a portion of the tile is
# present within the polygon. This needs to be updated to use something more reliable like:
# https://towardsdatascience.com/geofencing-with-quadkeys-7c5b9866ff98
def tiles_in_polygon(polygon, zoom):
    minx, miny, maxx, maxy = polygon.bounds
    min_tile_x, min_tile_y = latlon_to_tile(miny, minx, zoom)  # Note the swapped order
    max_tile_x, max_tile_y = latlon_to_tile(maxy, maxx, zoom)  # Note the swapped order
    tiles = []
    for x in range(min_tile_x, max_tile_x + 1):
        for y in range(max_tile_y,min_tile_y + 1):
            min_lat, min_lon = point_in_tile_to_latlon(x, y, 0, 0, zoom)  # Lower left corner
            max_lat, max_lon = point_in_tile_to_latlon(x, y, 1, 1, zoom)  # Upper right corner
            tile = box(min_lon, min_lat, max_lon, max_lat)  # Create box

            if polygon.intersects(tile):
                tiles.append((x, y))
    return tiles