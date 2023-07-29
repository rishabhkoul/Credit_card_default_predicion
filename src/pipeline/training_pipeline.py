from src.logger import logging
from src.exception import SrcException
from src import utility
import os,sys
from src.entity import config_entity,artifact_entity
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher


def start_training_pipeline():
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()

        #data ingestion
        data_ingestion_congfig = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        logging.info(data_ingestion_congfig.to_dict())

        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_congfig)
        data_ingestion_artifact = data_ingestion.initiate_data_ingesion()

        #Data validation
        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact= data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()

        #data transformation
        data_transformation_config = config_entity.DataTranformationConfig(training_pipeline_config=training_pipeline_config)
        data_transforamtion = DataTransformation(data_transformation_config=data_transformation_config, data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transforamtion.initiate_data_transformation()

        #model trainer
        model_trainer_config = config_entity.ModeltrainerConfig(training_pipeline_config = training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config = model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()

        #model evaluation
        model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_eval = ModelEvaluation(model_eval_config=model_eval_config, data_ingestion_artifact=data_ingestion_artifact, data_transformation_artifact=data_transformation_artifact, model_trainer_artifact=model_trainer_artifact)
        model_eval_artifact = model_eval.initiate_model_evaluation()

        #model pusher
        model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config=training_pipeline_config)
        model_pusher = ModelPusher(model_pusher_config=model_pusher_config, data_transformation_artifact=data_transformation_artifact, model_trainer_artifact=model_trainer_artifact)
        model_pusher_artifact = model_pusher.initiate_model_pusher()
    except Exception as e:
        raise SrcException(e,sys)
