from services.fetch import fetch
from services.upload import upload
from services.shared.constants import NEW_NORFOLK_BOUNDING_BOX
from services.detect import detect
from services.shared.constants import POSTGRES_URL
from sqlalchemy import create_engine
from geoalchemy2 import Geometry


files = fetch(geo_shape=NEW_NORFOLK_BOUNDING_BOX, resolution=18, limit=100)

# upload(bucket="NewNorfolk", files=files)

# files = download(bucket="NewNorfolk", dir="06-08-2023")

results = detect(files)

#  ----- Write to DB ------
engine = create_engine(POSTGRES_URL)

# Write DataFrame to PostGIS table "trees"
results.to_sql(
    "trees",
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
