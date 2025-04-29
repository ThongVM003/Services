import minio
from tqdm import tqdm

# Initialize minioClient with an endpoint and access/secret keys.
minioClient = minio.Minio(
    "192.168.103.219:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,
)

bucket = "security-events"

# Delete all objects in the bucket.
objects = minioClient.list_objects(bucket, recursive=True)
objects = list(objects)
for obj in tqdm(objects, desc="Deleting objects", colour="green", unit="objects"):

    # Delete object.
    minioClient.remove_object(bucket, obj.object_name)

# Delete bucket.
minioClient.remove_bucket(bucket)
