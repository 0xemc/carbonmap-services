from services.fetch import fetch
from services.detect import detect
from services.upload import upload
from shared.constants import POSTGRES_URL
from shared.utils.date import todays_date
from geoalchemy2 import Geometry
from sqlalchemy import (
    create_engine,
)
from shared.utils.supabase import db_client, upload_file

#  ----- Config------ #
RESOLUTION = 18
LIMIT = 500  # The maximum number of tiles to fetch
TODAY = todays_date()

#  ----- Fetch imagery ------ #
response = db_client.table("segments").select("*").eq("id", "GROVE_OF_GIANTS").execute()
bounding_box = response.data[0]["data"]

files = fetch(geo_shape=bounding_box, resolution=RESOLUTION, limit=LIMIT)
# upload(
#     bucket=f"GROVE_OF_GIANTS",
#     destination_dir=f"{todays_date()}-{RESOLUTION}",
#     files=files,
# )

# files = download(bucket="NewNorfolk", dir="06-08-2023")

#  ----- Predict ------ #
results = detect(files)
# Round lat and lon to 6 decimal places
results["lat"] = results["lat"].round(6)
results["lon"] = results["lon"].round(6)
results["date"] = TODAY


#  ----- Write to DB ------ #
engine = create_engine(POSTGRES_URL)
# Write DataFrame to PostGIS table "trees"
results.to_sql(
    f"trees",
    engine,
    if_exists="replace",
    index=False,
    dtype={"geom": Geometry("POINT", srid=4326)},
)
