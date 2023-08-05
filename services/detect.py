import concurrent.futures
import pandas as pd
from shared.utils.predict import predict_tile_img
from shared.constants import (
    POSTGRES_URL,
)
from sqlalchemy import create_engine
from geoalchemy2 import Geometry

# -------  Find the Trees  -------- #
# Create a ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Use list comprehension to create a list of futures
    futures = [
        executor.submit(predict_tile_img, image_file) for image_file in image_files
    ]

    # Collate the results into a single array
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

    merged_results = pd.concat(results, ignore_index=True)

print(merged_results)

#  ----- Write to DB ------
engine = create_engine(POSTGRES_URL)

# Write DataFrame to PostGIS table "trees"
merged_results.to_sql(
    "trees",
    engine,
    if_exists="append",
    index=False,
    dtype={"geom": Geometry("POINT", srid=4326)},
)
