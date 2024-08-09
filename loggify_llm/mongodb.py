import os
import pymongo
from dotenv import load_dotenv
from urllib.parse import quote_plus
from datetime import datetime
import zlib
import copy
import json
import pandas as pd

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
    def estimate_cost(self, records: list):
        """
        Estimates the total cost of using various language models based on token usage.

        This function calculates the cost associated with using different language models
        (LLMs) by considering the number of prompt and completion tokens used, along with
        the associated cost per token for each model. The cost is calculated in dollars 
        based on a pricing structure defined for each model.

        Args:
            records (list): A list of dictionaries where each dictionary contains information
                            about the usage of an LLM, including the model name (`llm_model`), 
                            the number of prompt tokens used (`prompt_tokens`), and the number 
                            of completion tokens generated (`completion_tokens`).

        Returns:
            float: The total estimated cost in dollars for using the LLMs across all records.
        """
        # Pricing per 1M tokens for different models
        # Ref: https://openai.com/api/pricing/
        unit_cost = {
            "gpt-3.5-turbo": {
                "prompt_tokens": 3,
                "completion_tokens": 6,
            },
            "gpt-4o-mini-2024-07-18**": {
                "prompt_tokens": 0.3,
                "completion_tokens": 1.2,
            },
            "gpt-4-vision-preview": {
                "prompt_tokens": 10,
                "completion_tokens": 30,
            }
        }
        # Convert the records list into a DataFrame for easier processing
        df_total = pd.DataFrame(records)
        
        # Get a list of unique LLM models used in the records
        unique_llm_models = df_total["llm_model"].unique().tolist()
        
        # Initialize the total cost to zero
        total_cost = 0
        
        # Loop through each LLM model to calculate the cost
        for llm_model in unique_llm_models:
            df_ = df_total[df_total["llm_model"] == llm_model]
            
            # Calculate the cost for prompt tokens
            prompt_tokens_cost = df_["prompt_tokens"].sum() * unit_cost[llm_model]["prompt_tokens"] * 1e-6
            
            # Calculate the cost for completion tokens
            completion_tokens_cost = df_["completion_tokens"].sum() * unit_cost[llm_model]["completion_tokens"] * 1e-6
            
            # Add the calculated costs to the total cost
            total_cost += prompt_tokens_cost
            total_cost += completion_tokens_cost

        # Return the total estimated cost in dollars
        return total_cost