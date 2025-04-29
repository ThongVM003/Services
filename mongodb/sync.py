import pymongo
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


# Copy a database from one MongoDB server to another
def copy_database(source_uri, target_uri, db_name, max_workers=4):
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
        documents = list(source_collection.find())
        if documents:
            with ThreadPoolExecutor(max_workers=max_workers) as doc_executor:
                list(
                    tqdm(
                        doc_executor.map(target_collection.insert_one, documents),
                        total=len(documents),
                        desc=f"Copying {collection_name}",
                        leave=False,
                    )
                )

    collection_names = source_db.list_collection_names()
    for collection_name in tqdm(collection_names, desc="Collections"):
        copy_collection(collection_name)

    # Close the connections
    source_client.close()
    target_client.close()


if __name__ == "__main__":
    source_uri = "mongodb://192.168.101.4:27017"
    target_uri = "mongodb://100.97.215.77:27017"
    db_name = "Orion"
    copy_database(source_uri, target_uri, db_name, max_workers=20)
