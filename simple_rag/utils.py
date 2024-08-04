import os
import pymongo
from dotenv import load_dotenv
from urllib.parse import quote_plus
import datetime

load_dotenv()


def connect_to_database():
    """
    Connects to a MongoDB database using credentials and connection details stored in environment variables.

    Environment Variables:
        COLLECTION_NAME (str): The name of the collection to connect to.
        DB_NAME (str): The name of the database.
        CLUSTER_ADDRESS (str): The address of the MongoDB cluster.
        USRNAME (str): The username for authentication, which will be URL-encoded.
        PASSWD (str): The password for authentication, which will be URL-encoded.

    Returns:
        pymongo.collection.Collection: The MongoDB collection object.

    Prints:
        str: Success message upon successful connection to the database.
    """
    collection_name = os.getenv("COLLECTION_NAME")
    db_name = os.getenv("DB_NAME")
    cluster_address = os.getenv("CLUSTER_ADDRESS")
    usrname = quote_plus(os.getenv("USRNAME"))
    passwd = quote_plus(os.getenv("PASSWD"))
    mongo_uri = f"mongodb+srv://{usrname}:{passwd}@{cluster_address}/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    print("🔥 Successfully Get Access Database")
    return collection


def insert_to_db(collection, data: dict):
    """
    Inserts specified keys and a timestamp into a MongoDB collection.

    Args:
        collection (pymongo.collection.Collection): The MongoDB collection to insert data into.
        data (dict): A dictionary containing the data to be inserted. Must contain the keys 'request_id', 'completion_tokens', 'prompt_tokens', and 'total_tokens'.

    Returns:
        None

    Prints:
        str: Success message upon successful insertion.
        str: Failure message if insertion fails, along with the exception message.
    """
    keys_to_extract = ["request_id", "completion_tokens", "prompt_tokens", "total_tokens"]
    data = {key: data[key] for key in keys_to_extract}
    time = datetime.datetime.now()
    time = str(time).replace(" ", "-")
    time = time.split(".")[0]
    data["time"] = time
    try:
        collection.insert_one(data)
        print("🔥 Successfully Log Request to Database")
    except Exception as e:
        print(f"👾 Fail To Log Request to Database because {e}")
