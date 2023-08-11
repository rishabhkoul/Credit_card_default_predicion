from src.exception import SrcException
from src.logger import logging
from src.entity import config_entity,artifact_entity
from src import utility
from src.predictor import ModelResolver
import os,sys


class ModelPusher:
    def __init__(self,model_pusher_config,data_transformation_artifact,model_trainer_artifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)
        except Exception as e:
            raise SrcException(e,sys)

    def initiate_model_pusher(self):
        try:
            logging.info('Loading Model and transformer')
            model = utility.load_object(file_path=self.model_trainer_artifact.model_path)
            
            logging.info(f"saving model into model pusher directory")
            utility.save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)

            logging.info(f"Saving model in saved model dir")
            model_path = self.model_resolver.get_latest_save_model_path()

            utility.save_object(file_path=model_path, obj=model)


            # prepare model_pusher artifact
            model_pusher_artifact = artifact_entity.ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir, saved_model_dir=self.model_pusher_config.saved_model_dir)
            logging.info(f"modelpusher artifact : {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise SrcException(e,sys)