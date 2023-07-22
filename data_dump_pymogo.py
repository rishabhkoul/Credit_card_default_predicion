import pymongo
import pandas as pd
import json


client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

DATABASE_NAME = "credit_card_data"
COLLECTION_NAME = "credit_default"
DATA_FILE_PATH = "/config/workspace/UCI_Credit_Card.csv"


if __name__== "__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns of dataframe is {df.shape}")
    # convert data into JSON format
    df.reset_index(drop = True, inplace=True)

    json_records = list(json.loads(df.T.to_json()).values())

    print(json_records[0])

    # insert the json formatted data to mongoDB
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_records)


