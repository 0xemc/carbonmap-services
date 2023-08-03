import os

# Mapbox API Key
API_KEY = os.environ.get("API_MAPBOX_KEY")

POSTGRES_URL = os.environ.get("API_NEON_URL")

MT_WELLINGTON_BOUNDING_BOX = [
    [147.207236314366, -42.82174924133314],
    [147.33247768190245, -42.89108351917231],
    [147.24496979008666, -42.98564101114084],
    [147.1281983746964, -42.910794494042634],
]

NEW_NORFOLK_BOUNDING_BOX = [
    [146.989113, -42.766299],
    [146.993496, -42.760242],
    [147.001283, -42.763971],
    [146.996333, -42.771259],
]


# Yaizu Court Bounding Box
BOUNDING_BOX = (147.2777, -42.8645, 147.279, -42.8639)

YAIZU_TILE = (18, 238316, 165684)
