import os
from services.shared.utils.geo import (
    kml_to_gpd,
    extract_boundaries,
    to_bounding_box,
)
from services.shared.utils.supabase import upload_file, insert

# upload_file(bucket="KML_812", destination="KML_812.kml", source="./KML_812.kml")
gpd = kml_to_gpd("./KML_812.kml")
gpd = extract_boundaries(gpd)
bb = to_bounding_box(gpd)

insert("segments", {"id": "KML_812", "data": bb, "description": "Test"})
print(bb)

if os.getenv("DEBUG") == "TRUE":
    with open("kml_812.geojson", "w") as f:
        f.write(str(gpd.to_json()))
