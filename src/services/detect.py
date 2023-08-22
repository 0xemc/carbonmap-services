import concurrent.futures
import pandas as pd
from services.shared.utils.predict import predict_tile_img


def detect(image_files: list[str]) -> pd.DataFrame:
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

    return merged_results
