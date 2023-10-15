import os
import zipfile
from typing import List, TypedDict
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

url: str = os.environ.get("API_SUPABASE_URL")
key: str = os.environ.get("API_SUPABASE_SERVICE_KEY")

db_client: Client = create_client(url, key, ClientOptions(postgrest_client_timeout=180))


def upload_file(bucket: str, source: str, destination: str, force: bool = False):
    bucket_list = [b.name for b in db_client.storage.list_buckets()]
    if bucket not in bucket_list:
        db_client.storage.create_bucket(bucket)
        print(f"Created bucket with name {bucket}")

    existing_files = [file["name"] for file in db_client.storage.from_(bucket).list()]

    if force or destination not in existing_files:
        db_client.storage.from_(bucket).upload(
            destination, source, file_options={"x-upsert": "true" if force else "false"}
        )
        print(f"Uploaded {source} to {destination}")
    else:
        print(f"Did not upload {destination} already exists")


class FileDict(TypedDict):
    source: str
    destination: str


def batch_upload_file(bucket: str, destination_dir: str, file_list: List[FileDict]):
    # Grab the existing files
    existing_files = [
        file["name"] for file in db_client.storage.from_(bucket).list(destination_dir)
    ]

    # For each file in file_list
    for file in file_list:
        # Define the source and destination
        source = file["source"]
        destination = file["destination"]

        # Check for existing file
        if destination not in existing_files:
            # Start a new thread to upload the file
            try:
                upload_file(bucket, source, f"{destination_dir}/{destination}")
            except Exception as e:
                print(f"An error occurred while uploading {destination}: {e}")
        else:
            print(f"File {destination} found in the bucket.")

    return "Success"


def zip_files(file_paths, dest_zip):
    with zipfile.ZipFile(dest_zip, "w") as zipf:
        for file in file_paths:
            zipf.write(file)


def download_file(bucket: str, file: str, output_dir: str):
    with open(f"{output_dir}/{file}", "wb+") as f:
        res = db_client.storage.from_(bucket).download(file)
        f.write(res)


# def batch_retrieve(bucket: str, file_list: List[FileDict], output_dir: str):
#     # Grab the existing files
#     existing_files = os.listdir(output_dir)

#     # For each file in file_list
#     for file in file_list:
#         # Define the source and destination
#         source = file["source"]
#         destination = file["destination"]

#         # Check for existing file
#         if destination in existing_files:
#             print(f"File {destination} already exists.")
#             continue

#         # Start a new thread to download the file
#         try:
#             with open(f"{output_dir}/{destination}", "wb+") as f:
#                 res = supabase.storage.from_(bucket).download(source)
#                 f.write(res)
#             print(f"Downloaded {source} to {destination}")
#         except Exception as e:
#             print(f"An error occurred while downloading {source}: {e}")
