import os

from supabase import create_client, Client

url: str = os.environ.get("API_SUPABASE_URL")
key: str = os.environ.get("API_SUPABASE_SERVICE_KEY")
supabase: Client = create_client(url, key)

bucket_name = "TEST"
destination = "/tmp/tile_238106_165585_18.jpg"

bucket_exists = supabase.storage.get_bucket(bucket_name)
if not bucket_exists:
    supabase.storage.create_bucket(bucket_name)

file_list = supabase.storage.from_(bucket_name).list()

if destination not in [file["name"] for file in file_list]:
    print(f"File {destination} not found in the bucket.")

supabase.storage.from_(bucket_name).upload(
    destination, "/tmp/images/tile_238106_165585_18.jpg"
)
