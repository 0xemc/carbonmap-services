import os
from services.shared.utils.geo import (
    kml_to_gpd,
    extract_boundaries,
    to_bounding_box,
)

gpd = kml_to_gpd("./KML_812.kml")
gpd = extract_boundaries(gpd)
bb = to_bounding_box(gpd)


if os.getenv("DEBUG") == "TRUE":
    with open("kml_812.geojson", "w") as f:
        f.write(str(gpd.to_json()))
