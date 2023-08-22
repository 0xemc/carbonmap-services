import os
from typing import List

BoundingBox = List[List[float]]

# Mapbox API Key
API_KEY = os.environ.get("API_MAPBOX_KEY")

# Supabase POSTGRES url
POSTGRES_URL = os.environ.get("API_SUPABASE_POSTGRES_URL")
