from src.logger import logging
from src.exception import SrcException
import sys,os
from src.utility import get_collections_as_dataframe
from src.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from src.components.data_ingestion import DataIngestion

if __name__ == "__main__":
     try:
          training_pipeline_config = TrainingPipelineConfig()
          data_ingestion_config = DataIngestionConfig(training_pipeline_config)
          print(data_ingestion_config.to_dict())
          data_ingestion = DataIngestion(data_ingestion_config)
          print(data_ingestion.initiate_data_ingesion())


     except Exception as e:
          raise SrcException(e,sys)
