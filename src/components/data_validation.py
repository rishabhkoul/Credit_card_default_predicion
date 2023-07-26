from src.logger import logging
from src.exception import SrcException
from src.components import data_ingestion
from src.entity import config_entity,artifact_entity
from src import utility, config
import os,sys
import pandas as pd 
import numpy as np 
from src.config import TARGET_COLUMN


class DataValidation:

    def __init__(self,data_validation_config:config_entity.DataValidationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
        except Exception as e:
            raise SrcException(e,sys)
    
    def required_column_exists(self,base_df,current_df,report_key_name) -> bool:
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns

            missing_columns = []
            for i in base_columns:
                if i not in current_columns:
                    logging.info(f'column: [{i}] is not available')
                    missing_columns.append(i)

            if len(missing_columns) > 0:
                self.validation_error[report_key_name] = missing_columns
                return False
            return True

        except Exception as e:
            raise SrcException(e,sys) 

    



    def initiate_data_validation(self) -> artifact_entity.DataValidationArtifact:
        try:
            logging.info('Reading Base Dataframe')

            base_df = pd.read_csv(self.data_validation_config.base_df_path)

            logging.info("Reading Train DataFrame")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info("Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            exclude_column = [TARGET_COLUMN]

            logging.info(f"Checking if required columns exist in train_df")
            train_df_columns_status = self.required_column_exists(base_df, train_df, report_key_name="missing_columns_train")
            logging.info("Checking if required columns exist in test_df")
            test_df_columns_status = self.required_column_exists(base_df, test_df, report_key_name="missing_columns_test")

            if train_df_columns_status:
                logging.info("All required columns are available in train df")
            
            if test_df_columns_status:
                logging.info("All required columns are avaiable in the test dataframe")

            #writing the report
            logging.info("writing report in yaml file")
            utility.write_yaml_file(self.data_validation_config.report_file_path,self.validation_error)

            # preparing validation artifact
            data_validation_artifact = artifact_entity.DataValidationArtifact(self.data_validation_config.report_file_path)
            loggung.info(f"Data Validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise SrcException(e,sys)