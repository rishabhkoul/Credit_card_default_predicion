from src.logger import logging
from src.exception import SrcException
from src import utility
from src.entity import artifact_entity,config_entity
import pandas as pd 
import numpy as np 
import os,sys 
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from imblearn.combine import SMOTETomek
from sklearn.preprocessing import RobustScaler
from src.config import TARGET_COLUMN

class DataTransformation:
    def __init__(self,data_transformation_config:config_entity.DataTranformationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>'*20} Data tranformation {'<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise SrcException(e,sys)
        
    def initiate_data_transformation(self):
        try:
            #reading training and testing files
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)     

            #Selecting input features for train and test DataFrames
            input_features_train_df = train_df.drop(TARGET_COLUMN,axis=1)
            input_features_test_df = test_df.drop(TARGET_COLUMN,axis=1)

            # Selecing target column for train and test dataset
            target_feature_train = train_df[TARGET_COLUMN]
            target_feature_test = test_df[TARGET_COLUMN]

            #Scaling the data
            scaler = RobustScaler()
            scaler.fit(input_features_train_df)

            input_features_train_arr = scaler.transform(input_features_train_df)
            input_features_test_arr = scaler.transform(input_features_test_df)

            smt = SMOTETomek(random_state=42)
            logging.info(f"Before resampling in training dataset Input: {input_features_train_arr.shape} target: {target_feature_train}")
            input_features_train_arr,target_feature_train = smt.fit_resample(input_features_train_arr,target_feature_train)
            logging.info(f"After resampling in training set input:{input_features_train_arr} target: {target_feature_train}")

            logging.info(f"Before resampling Test dataset Input:{input_features_test_arr} Target:{target_feature_test}")
            input_features_test_arr,target_feature_test = smt.fit_resample(input_features_test_arr,target_feature_test)
            logging.info(f"After resampling in training set input:{input_features_test_arr} target: {target_feature_test}")

            train_arr = np.c_[input_features_train_arr,target_feature_train]
            test_arr = np.c_[input_features_test_arr,target_feature_test]

            utility.save_numpy_array_data(self.data_transformation_config.transformed_train_path, train_arr)
            utility.save_numpy_array_data(self.data_transformation_config.transformed_test_path, test_arr)


            data_transformation_artifact = artifact_entity.DataTranformationArtifact(
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path
            )
            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise SrcException(e, sys)
