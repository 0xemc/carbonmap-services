import os
from typing import List, TypedDict
from supabase import create_client, Client

from concurrent.futures import ThreadPoolExecutor

url: str = os.environ.get("API_SUPABASE_URL")
key: str = os.environ.get("API_SUPABASE_SERVICE_KEY")

supabase: Client = create_client(url, key)


def store(bucket: str, source: str, destination: str):
    bucket_list = [b.name for b in supabase.storage.list_buckets()]
    if bucket not in bucket_list:
        supabase.storage.create_bucket(bucket)
        print(f"Created bucket with name {bucket}")

    supabase.storage.from_(bucket).upload(destination, source)
    print(f"Uploaded {source} to {destination}")


class FileDict(TypedDict):
    source: str
    destination: str


def batch_store(bucket: str, destination_dir: str, file_list: List[FileDict]):
    # Grab the existing files
    existing_files = [
        file["name"] for file in supabase.storage.from_(bucket).list(destination_dir)
    ]

    # For each file in file_list
    for file in file_list:
        # Define the source and destination
        source = file["source"]
        destination = file["destination"]

        # Check for existing file
        if destination in existing_files:
            print(f"File {destination} found in the bucket.")
            continue

        # Start a new thread to upload the file
        try:
            store(bucket, source, f"{destination_dir}/{destination}")
        except Exception as e:
            print(f"An error occurred while uploading {destination}: {e}")
