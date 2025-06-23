import pymongo
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


# Copy a database from one MongoDB server to another
def copy_database(
    source_uri, target_uri, db_name, collection_names=None, max_workers=4
):
    # Connect to the source MongoDB server
    source_client = pymongo.MongoClient(source_uri)
    source_db = source_client[db_name]

    # Connect to the target MongoDB server
    target_client = pymongo.MongoClient(target_uri)
    target_db = target_client[db_name]

    def copy_collection(collection_name):
        source_collection = source_db[collection_name]
        target_collection = target_db[collection_name]
        target_collection.drop()
        print(f"Copying collection: {collection_name}")
        documents = source_collection.find()
        if documents:
            with ThreadPoolExecutor(max_workers=max_workers) as doc_executor:
                list(
                    tqdm(
                        doc_executor.map(target_collection.insert_one, documents),
                        # total=len(documents),
                        desc=f"Copying {collection_name}",
                        leave=True,
                    )
                )

    if collection_names is None:
        # If no specific collections are provided, copy all collections
        collection_names = source_db.list_collection_names()
    for collection_name in collection_names:
        copy_collection(collection_name)

    # Close the connections
    source_client.close()
    target_client.close()


if __name__ == "__main__":
    source_uri = "mongodb://AdminSammy:ttsxtm@103.129.80.172:27017/?authSource=admin&readPreference=primary&directConnection=true&ssl=false"
    source_uri = "mongodb://hoanghoa:IgJp9cSOym5Py8o@192.168.255.202:27017,192.168.255.208:27017/?replicaSet=rs0&authSource=admin"
    target_uri = "mongodb://100.106.39.74:27017"
    db_name = "security"
    collection_names = ["LicensePlateDetection"]
    copy_database(
        source_uri,
        target_uri,
        db_name,
        collection_names=collection_names,
        max_workers=20,
    )
