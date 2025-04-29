import minio
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from rich import print
import datetime

# Initialize minioClient with an endpoint and access/secret keys.
minioClient = minio.Minio(
    "192.168.101.2:9000",
    access_key="becamex",
    secret_key="becamex@123",
    secure=False,
)

path = "alert-security-events/lpr_detected"
bucket = path.split("/")[0]
prefix = "/".join(path.split("/")[1:])

print(f"Deleting all objects in bucket '{bucket}' with prefix '{prefix}'.")

# Delete all objects in the bucket.
objects = minioClient.list_objects(bucket, prefix=prefix, recursive=True)
# objects = list(objects)


# print(f"Found {len(objects)} objects to delete.")

# Define the date to compare against.
date = "1/3/2025"
date = datetime.datetime.strptime(date, "%d/%m/%Y")
# Make the `date` timezone-aware (UTC).
date = date.replace(tzinfo=datetime.timezone.utc)


def delete_object(obj):
    """Delete a single object."""
    # Check if the object is older than the specified date.
    # 2025-03-26 09:44:39.426000+00:00
    obj_date = obj.last_modified
    obj_date = datetime.datetime.strptime(str(obj_date), "%Y-%m-%d %H:%M:%S.%f%z")
    # print(f"Object date: {obj_date} - Comparing with date: {date}")

    if obj_date < date:
        print(f"[red]Deleting object: {obj.object_name}[/red]")

        minioClient.remove_object(bucket, obj.object_name)


# Use ThreadPoolExecutor for parallel deletion.
with ThreadPoolExecutor() as executor:
    list(
        tqdm(
            executor.map(delete_object, objects),
            desc="Deleting objects",
            colour="green",
            unit="objects",
            # total=len(objects),
        )
    )

# # Delete bucket (uncomment if needed).
# minioClient.remove_bucket(bucket)
