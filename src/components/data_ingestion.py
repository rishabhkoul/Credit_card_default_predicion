from src.logger import logging
from src.exception import SrcException
from src.utility import get_collections_as_dataframe
from src.entity import config_entity, artifact_entity
import os,sys
import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SrcException(e,sys)

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"Exporting collection data from mongoDB as pandas Dataframe")
            df = get_collections_as_dataframe(self.data_ingestion_config.database_name, self.data_ingestion_config.collection_name)

            logging.info(f"Saving dataset in feature store folder")

            logging.info(f"Creating feature store folder if not available")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)

            logging.info("Save df to feature store folder")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)      

            logging.info("Splitting the data set into train and test")


            train_df,test_df = train_test_split(df,test_size = self.data_ingestion_config.test_size,random_state = 42)

            logging.info(f"Creating dataset directory if not available")

            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok = True)
            
            logging.info("Saving train and test files into dataset folder ")

            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)

            # Preparing artifact

            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(train_file_path=self.data_ingestion_config.train_file_path, test_file_path= self.data_ingestion_config.test_file_path, feature_store_file_path = self.data_ingestion_config.feature_store_file_path)
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise SrcException(e,sys)