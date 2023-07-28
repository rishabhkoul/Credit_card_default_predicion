import pandas as pd 
from src.config import mongo_client
from src.logger import logging
from src.exception import SrcException
import os, sys
import yaml
import dill


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

def write_yaml_file(file_path,data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok = True)

        with open(file_path,'w') as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise SrcException(e, sys)
def save_object(file_path,obj):
    try:
        logging.info("Entered the save object method of utility")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)

        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj)
        logging.info("Exited the save object method of utility")
        
    except Exception as e:
        raise SrcException(e,sys)

def load_object(file_path):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"the file {file_path} does not exist")
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise SrcException(e,sys)

def save_numpy_array_data(file_path,array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok =True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise SrcException(e,sys)

def load_numpy_array_data(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SrcException(e,sys)
