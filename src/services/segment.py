import os
import argparse
from shared.utils.geo import (
    kml_to_gpd,
    extract_boundaries,
    to_bounding_box,
    geojson_to_gpd,
)
from shared.utils.supabase import upload_file, db_client

parser = argparse.ArgumentParser(description="Create a new segment.")

# Add the arguments
parser.add_argument(
    "--file", type=str, required=True, help="Path to geojson or kml file"
)
parser.add_argument("--id", type=str, required=True, help="ID of the segment")
parser.add_argument("--description", type=str, help="Optional description")
parser.add_argument("--debug", action="store_true", help="Optional debug flag")

# Parse the arguments
args = parser.parse_args()

file_path = args.file
segment_id = args.id
segment_description = args.description

# Store the segment definition
upload_file(
    bucket=segment_id, destination=os.path.basename(file_path), source=file_path
)

# Convert to GeoPandas Data Frame
file_extension = os.path.splitext(file_path)[1]
transform_fn = kml_to_gpd if file_extension == ".kml" else geojson_to_gpd
gpd = transform_fn(file_path)

# Merge all sections and calculate the boundary
gpd = extract_boundaries(gpd)

# Convert it to a BoundingBox
bb = to_bounding_box(gpd)

# Add to the DB
query = db_client.table("segments").upsert(
    {"id": segment_id, "data": bb, "description": segment_description}
)
query.execute()

if args.debug:
    with open("debug.geojson", "w") as f:
        f.write(str(gpd.to_json()))
