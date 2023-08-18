from services.shared.utils.geo import (
    kml_to_gpd,
    extract_boundaries,
    to_bounding_box,
)

gpd = kml_to_gpd("./KML_812.kml")
gpd = extract_boundaries(gpd)
bb = to_bounding_box(gpd)

print(gpd.to_geojson())
