# Batch download images from a list of URLs
import os
from minio import Minio
from tqdm.rich import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich import print

client = Minio(
    "192.168.101.4:19000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,
)

DIR = "sharefile/plate"
out_dir = "data"
os.makedirs(out_dir, exist_ok=True)

bucket = DIR.split("/")[0]
prefix = "/".join(DIR.split("/")[1:])


objects = client.list_objects(
    bucket,
    prefix=prefix,
    recursive=True,
)


object_names = [obj.object_name for obj in objects]
print(f"Found {len(object_names)} objects")

# max_pic = input("Enter max number of images to download: ")
# max_pic = int(max_pic)

# if len(object_names) > max_pic:
#     object_names = object_names[:max_pic]
#     print(f"Download only {max_pic} images")

max_workers = 20


def download_object(object_name):
    # object_dir = os.path.dirname(object_name)
    # os.makedirs(f"data/{object_dir}", exist_ok=True)
    # tqdm.write(f"Downloading {object_name}")
    client.fget_object(bucket, object_name, f"data/{object_name}")


with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [
        executor.submit(download_object, object_name) for object_name in object_names
    ]
    for future in tqdm(
        as_completed(futures), total=len(futures), desc="Downloading files"
    ):
        future.result()
