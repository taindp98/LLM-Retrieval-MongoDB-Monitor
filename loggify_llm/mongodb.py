import os
import pymongo
from dotenv import load_dotenv
from urllib.parse import quote_plus
from datetime import datetime
import zlib
import copy
import json

load_dotenv()


class MongoDBLogger:
    def __init__(self) -> None:
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
        mongo_uri = (
            f"mongodb+srv://{usrname}:{passwd}@{cluster_address}/?retryWrites=true&w=majority"
        )
        client = pymongo.MongoClient(mongo_uri)
        db = client[db_name]
        self.collection = db[collection_name]
        print("🔥 Successfully Get Access Database")
        self.keys_need_compress = ["input", "output"]

    def _compress_messages(self, messages):
        messages = json.dumps(messages)
        compressed_msg = zlib.compress(messages.encode("utf-8"))
        return compressed_msg

    def _decompress_messages(self, compressed_messages):
        decompressed_msg = zlib.decompress(compressed_messages).decode("utf-8")
        return decompressed_msg

    def insert_to_db(self, data: dict):
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
        insert_data = copy.copy(data)
        for k in list(insert_data.keys()):
            if k in self.keys_need_compress:
                insert_data[k] = self._compress_messages(insert_data[k])

        insert_data["time"] = datetime.utcnow()
        try:
            self.collection.insert_one(insert_data)
            print("🔥 Successfully Log Request to Database")
        except Exception as e:
            print(f"👾 Fail To Log Request to Database because {e}")

    def query_collection(self, query: dict = {}):
        """
        Queries the MongoDB collection with the specified query.

        Args:
            query (dict): The MongoDB query.

        Returns:
            list: A list of documents that match the query.
        """
        raw_results = list(self.collection.find(query))
        fine_results = []
        for res in raw_results:
            for k in list(res.keys()):
                if k in self.keys_need_compress:
                    res[k] = self._decompress_messages(res[k])
            fine_results.append(res)
        return fine_results
