import os
from shared.utils.supabase import batch_upload_file, FileDict


def upload(bucket: str, destination_dir: str, files: list[str]):
    # Create a list of FileDict from the above files
    file_dicts = [
        FileDict(source=file, destination=extract_filename(file)) for file in files
    ]

    # Store the files
    batch_upload_file(bucket, destination_dir, file_dicts)


def extract_filename(file_path: str) -> str:
    return os.path.basename(file_path)
