import os
from minio import Minio
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# MinIO client setup
client = Minio(
    "192.168.101.4:19000",
    secret_key="minioadmin",
    access_key="minioadmin",
    secure=False,
)

# Configuration
local_path = "/home/ghostm211/Projects/Work/Dev/PlateTrain/dataset"  # Local file or folder to upload
bucket_name = "sharefile"
minio_prefix = "plate"  # Target folder inside bucket
max_workers = 20  # Number of parallel uploads

# Ensure bucket exists
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)
    print(f"✅ Created bucket: {bucket_name}")

# Gather files to upload
files_to_upload = []

if os.path.isfile(local_path):
    object_name = os.path.join(minio_prefix, os.path.basename(local_path)).replace(
        "\\", "/"
    )
    files_to_upload.append((local_path, object_name))
else:
    for root, _, files in os.walk(local_path):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, local_path)
            object_name = os.path.join(minio_prefix, rel_path).replace("\\", "/")
            files_to_upload.append((full_path, object_name))


# Upload function
def upload_file(local_file, object_name):
    client.fput_object(bucket_name, object_name, local_file)


# Upload in parallel with progress
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [
        executor.submit(upload_file, local_file, object_name)
        for local_file, object_name in files_to_upload
    ]
    for _ in tqdm(as_completed(futures), total=len(futures), desc="Uploading to MinIO"):
        pass  # futures are awaited for completion

print(
    f"✅ Uploaded {len(files_to_upload)} files to bucket '{bucket_name}/{minio_prefix}'"
)
