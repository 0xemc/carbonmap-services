import os
import argparse
from shared.utils.geo import (
    kml_to_gpd,
    extract_boundaries,
    to_bounding_box,
    geojson_to_gpd,
)
from toolz import dissoc
import shapely.wkt
import shapely.geometry
import json
from geoalchemy2 import Geometry, WKTElement
from shared.utils.supabase import upload_file, db_client

parser = argparse.ArgumentParser(description="Create a new segment.")

# Add the arguments
parser.add_argument(
    "--file", type=str, required=True, help="Path to geojson or kml file"
)
parser.add_argument("--id", type=str, required=True, help="ID of the segment")
parser.add_argument("--description", type=str, help="Optional description")
parser.add_argument("--upsert", action="store_true", help="Override existing data")
parser.add_argument("--debug", action="store_true", help="Optional debug flag")

# Parse the arguments
args = parser.parse_args()

file_path = args.file
segment_id = args.id
segment_description = args.description
upsert = args.upsert

# Store the segment definition
upload_file(
    bucket=segment_id,
    destination=os.path.basename(file_path),
    source=file_path,
    force=upsert,
)

# Convert to GeoPandas Data Frame
file_extension = os.path.splitext(file_path)[1]
transform_fn = kml_to_gpd if file_extension == ".kml" else geojson_to_gpd
gpd = transform_fn(file_path)

# Merge all sections and calculate the boundary
# gpd = extract_boundaries(gpd)

# Convert it to a BoundingBox
# bb = to_bounding_box(gpd)

# Convert it to a GeoJSON
geojson = json.loads(gpd.to_json())

# Extract Polygon Features
features = []
for feature in geojson["features"]:
    if feature["geometry"]["type"] == "Polygon":
        features.append(feature)
    elif feature["geometry"]["type"] == "MultiPolygon":
        for polygon in feature["geometry"]["coordinates"]:
            new_feature = {
                **dissoc(feature, "geometry"),
                "geometry": {"coordinates": polygon, "type": "Polygon"},
            }
            features.append(new_feature)

# Convert each feature to a Shapely geometry and collect them in a list
coordinates = [
    shapely.Polygon(feature["geometry"]["coordinates"][0]) for feature in features
]
# Convert the list of geometries to a MultiPolygon
multipolygon = shapely.MultiPolygon(coordinates)

# Convert the MultiPolygon to WKT
wkt = shapely.wkt.dumps(multipolygon)

# Create a WKTElement
element = WKTElement(wkt, srid=4326)

# Add to the DB
segment_data = {
    "id": segment_id,
    "geom": str(element),
    "description": segment_description,
    "geojson": geojson,
}

try:
    query = (
        db_client.table("segments").upsert(segment_data)
        if upsert
        else db_client.table("segments").insert(segment_data)
    )
    result = query.execute()
except Exception as e:
    print(f"Error occurred during insert/upsert operation: {e}")


if args.debug:
    with open("debug.geojson", "w") as f:
        f.write(str(geojson))
