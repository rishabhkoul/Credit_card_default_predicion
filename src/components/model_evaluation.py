from src.predictor import ModelResolver
from src.logger import logging
from src.exception import SrcException
from src.entity import config_entity,artifact_entity
from src import predictor
import os,sys
from src import utility
from sklearn.metrics import f1_score
import pandas as pd 
from src.config import TARGET_COLUMN

class ModelEvaluation:
    def __init__(self,model_eval_config:config_entity.ModelEvaluationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact,data_transformation_artifact,model_trainer_artifact):
        try:
            logging.info(f"{'>'*20} Model evaluation {'<'*20}")
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise SrcException(e,sys)
    
    def initiate_model_evaluation():
        try:
            # if saved model folder has a model we will compare it to newer model
            # and check which model is best trained
            logging.info("If saved model folder has a model, then we will compare which model is best trained")
            latest_dir_path = self.model_resolver.get_latest_dir_path
            if latest_dir_path == None:
                model_eval_artifact_entity = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=None)
                logging.info(f"Model evalutation artifact: {model_eval_artifact_entity}")
            
            # Finding the location of model
            logging.info("Finding the location of model")
            model_path = get_latest_model_path()

            logging.info("Previous trained objects of model")
            model = utility.load_object(file_path=model_path)

            logging.info(f"currently trained model")
            current_model = utility.load_object(file_path=self.model_trainer_artifact.model_path)

            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df = test_df[TARGET_COLUMN]
            y_true = target_df

            y_pred = model.predict(test_df.drop(TARGET_COLUMN,axis=1))
            logging.info(f"Prediction using previous model: {y_pred[:5]}")
            previous_model_score = f1_score(y_true,y_pred)
            logging.info(f"Accuracy using previous trained model : {previous_model_score}")

            # accuracy using current trained model
            input_arr = test_df.drop(TARGET_COLUMN,axis=1)
            y_true = test_df[TARGET_COLUMN]
            y_pred = current_model.predict(input_arr)
            logging.info(f"prediction using trained model {y_pred[:5]}")

            current_model_score = f1_score(y_true,y_pred)
            logging.info(f"Accuracy using current trained model : {current_model_score}")

            if current_model_score <= previous_model_score:
                logging.info(f'current trained model is not better han pevious model')
                raise Exception(f'current trained model is not better han pevious model')

            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=current_model_score-previous_model_score)

            logging.info(f"model eval artifact: {model_eval_artifact}")
            return model_eval_artifact
        except Exception as e:
            raise SrcException(e,sys)