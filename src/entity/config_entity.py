import os,sys
from datetime import datetime
from src.exception import SrcException

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = 'target_encoder.pkl'
MODEL_FILE_NAME = 'model.pkl'

 
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
        

class DataTranformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,"data_transformation")
        self.transformer_object_path = os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_OBJECT_NAME)
        self.transformed_train_path = os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE_NAME.replace('csv','npz'))
        self.transformed_test_path = os.path.join(self.data_transformation_dir,'transformed',TEST_FILE_NAME.replace('csv','npz'))
        self.target_encoder_object_path = os.path.join(self.data_transformation_dir,'encoder',TARGET_ENCODER_OBJECT_FILE_NAME)


class ModeltrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir,"model_trainer")
        self.model_path = os.path.join(self.model_trainer_dir,MODEL_FILE_NAME)
        self.expected_score = 0.7
        self.overfitting_threshold = 0.1


class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.change_threshold = 0.01

class ModelPusherConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_pusher_dir = ps.path.join(training_pipeline_config.artifact_dir,'model_pusher')
        self.saved_model_dir = os.path.join("saved_models")
        self.pusher_model_dir = os.path.join(self.model_pusher_dir,'saved_models')
        self.pusher_model_path = os.path.join(self.pusher_model_dir,MODEL_FILE_NAME)
        self.pusher_transformer_path = os.path.join(self.pusher_model_dir,TRANSFORMER_OBJECT_NAME)
        