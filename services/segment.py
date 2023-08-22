import os
from services.shared.utils.geo import (
    kml_to_gpd,
    extract_boundaries,
    to_bounding_box,
)
from services.shared.utils.supabase import upload_file, db_client

# Store the KML file
upload_file(bucket="KML_812", destination="KML_812.kml", source="./KML_812.kml")

# Convert to GeoPandas Data Frame
gpd = kml_to_gpd("./KML_812.kml")

# Merge all sections and calculate the boundary
gpd = extract_boundaries(gpd)

# Convert it to a BoundingBox
bb = to_bounding_box(gpd)

# Add to the DB
db_client.table("segments").insert(
    {"id": "KML_812", "data": bb, "description": "Test"}
).execute()

if os.getenv("DEBUG") == "TRUE":
    with open("kml_812.geojson", "w") as f:
        f.write(str(gpd.to_json()))
