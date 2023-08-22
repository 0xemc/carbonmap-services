from services.fetch import fetch
from services.detect import detect
from services.shared.constants import POSTGRES_URL
from services.shared.utils.date import todays_date
from geoalchemy2 import Geometry
from sqlalchemy import (
    create_engine,
    Table,
    MetaData,
    Column,
    Float,
    PrimaryKeyConstraint,
)
from services.shared.utils.supabase import db_client

RESOLUTION = 18
LIMIT = 500
TODAY = todays_date()
metadata = MetaData()

response = db_client.table("segments").select("*").eq("id", "KML_812").execute()

bounding_box = response.data[0]["data"]
files = fetch(geo_shape=bounding_box, resolution=RESOLUTION, limit=LIMIT)
# upload(bucket=f"KML_812", destination_dir=f"{todays_date()}-{RESOLUTION}", files=files)

# files = download(bucket="NewNorfolk", dir="06-08-2023")
results = detect(files)

#  ----- Write to DB ------

# Define the table with the composite primary key of lat,lon to avoid double counting
table = Table(
    f"trees-{RESOLUTION}",
    metadata,
    Column("lat", Float),
    Column("lon", Float),
    # Other columns...
    PrimaryKeyConstraint("lat", "lon", name="lat_lon_pk"),
)

# Round lat and lon to 6 decimal places (1.11m resolution)
results["lat"] = results["lat"].round(6)
results["lon"] = results["lon"].round(6)
results["date"] = TODAY

print(results)

engine = create_engine(POSTGRES_URL)

# Write DataFrame to PostGIS table "trees"
results.to_sql(
    f"trees-{RESOLUTION}",
    engine,
    if_exists="replace",
    index=False,
    dtype={"geom": Geometry("POINT", srid=4326)},
)

# from sqlalchemy.sql import text

# with engine.connect() as connection:
#     connection.execute(text(f"""
#         CREATE TABLE IF NOT EXISTS bounding_boxes (
#             id SERIAL PRIMARY KEY,
#             bounding_box GEOMETRY(Polygon, 4326)
#         );
#         INSERT INTO bounding_boxes (bounding_box)
#         VALUES (ST_GeomFromText('POLYGON(({NEW_NORFOLK_BOUNDING_BOX}))', 4326));
#     """))
