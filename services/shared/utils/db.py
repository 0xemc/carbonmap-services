import os
from typing import List, TypedDict
from supabase import create_client, Client

from concurrent.futures import ThreadPoolExecutor

url: str = os.environ.get("API_SUPABASE_URL")
key: str = os.environ.get("API_SUPABASE_SERVICE_KEY")

supabase: Client = create_client(url, key)


def store(bucket: str, source: str, destination: str):
    bucket_exists = supabase.storage.get_bucket(bucket)
    if not bucket_exists:
        supabase.storage.create_bucket(bucket)

    supabase.storage.from_(bucket).upload(destination, source)


class FileDict(TypedDict):
    source: str
    destination: str


def batch_store(bucket: str, file_list: List[FileDict], workers=10):
    # Define the maximum number of concurrent requests
    MAX_WORKERS = workers

    # Grab the existing files
    file_list = supabase.storage.from_(bucket).list()

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # For each file in file_list
        for file in file_list:
            # Define the source and destination
            source = file["source"]
            destination = file["destination"]

            # Check for existing file
            if destination in [file["destination"] for file in file_list]:
                print(f"File {destination} not found in the bucket.")
                continue

            # Start a new thread to upload the file
            executor.submit(store, bucket, source, destination)
