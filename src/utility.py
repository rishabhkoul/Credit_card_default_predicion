import pandas as pd 
from src.config import mongo_client
from src.logger import logging
from src.exception import SrcException
import os, sys


def get_collections_as_dataframe(database_name,collection_name):
    try:
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Columns present in the database: {df.columns}")
        if "_id" in df.columns:
            logging.info(f'"Dropping column: _id')
            df = df.drop("_id",axis=1)
        logging.info(f"Rows and columns in the dataframe : {df.shape}")    
        return df
    except Exception as e:
        raise SrcException(e,sys)
