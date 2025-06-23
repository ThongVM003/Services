import datetime
import pymongo
import time
from rich import print


# source_uri = "mongodb://AdminSammy:ttsxtm@103.129.80.172:27017/?authSource=admin&readPreference=primary&directConnection=true&ssl=false"
# source_uri = "mongodb://hoanghoa:IgJp9cSOym5Py8o@192.168.255.202:27017,192.168.255.208:27017/?replicaSet=rs0&authSource=admin"
source_uri = "mongodb://100.106.39.74:27017"


client = pymongo.MongoClient(source_uri)
db = client["security"]
collection = db["LicensePlateDetection"]


# Query filter
query = {
    "DateTime": {
        "$gte": datetime.datetime(2025, 4, 1, 0, 0, 0),
        "$lt": datetime.datetime(2025, 6, 3, 0, 0, 0),
    },
    "LicensePlate": {"$regex": "^.*70L18.*$"},
    # "$text": {"$search": "61U22859"},
}

# Sort by DateTime descending
sort = [("DateTime", -1)]

count = 0
start_time = time.time()
results = collection.find(query).sort(sort).limit(100)
# count = collection.count_documents(query)
# count = len(list(results))
end_time = time.time()

get_start = time.time()
c = list(results)
get_end = time.time()

# Print number of results
print(f"Number of results: {count}")
# Print time taken for the query
print(f"Time taken for the query: {end_time - start_time:.2f} seconds")
print(f"Time taken to get results: {get_end - get_start:.2f} seconds")
