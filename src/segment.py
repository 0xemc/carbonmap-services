import os
from shared.utils.geo import (
    kml_to_gpd,
    extract_boundaries,
    to_bounding_box,
    geojson_to_gpd,
)
from shared.utils.supabase import upload_file, db_client

file_path = "./grove.geojson"

# Store the KML file
# upload_file(bucket="KML_812", destination="KML_812.kml", source=file_path)

# Convert to GeoPandas Data Frame
gpd = geojson_to_gpd(file_path)

# Merge all sections and calculate the boundary
gpd = extract_boundaries(gpd)

# Convert it to a BoundingBox
bb = to_bounding_box(gpd)


# Add to the DB
db_client.table("segments").insert(
    {"id": "GROVE_OF_GIANTS", "data": bb, "description": ""}
).execute()

if os.getenv("DEBUG") == "TRUE":
    with open("debug.geojson", "w") as f:
        f.write(str(gpd.to_json()))
