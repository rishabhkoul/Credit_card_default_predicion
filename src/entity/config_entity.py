import os,sys
from datetime import datetime
from src.exception import SrcException

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

 
class TrainingPipelineConfig:
    def __init__(self):
        # we create a folder where the arifacts(outputs) will be stored
        self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.database_name = "credit_card_data"
        self.collection_name = "credit_default"
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
        self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store")
        self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
        self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
        self.test_size = 0.2
    def to_dict(self):
        try:
            return self.__dict__
        except Exception as e:
            raise SrcException(e,sys)



class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir,"data_validation")
        self.base_df_path = os.path.join("UCI_Credit_Card.csv")
        self.report_file_path = os.path.join(self.data_validation_dir,"report.yaml")
        

class DataTranformationConfig:...
class ModeltrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...