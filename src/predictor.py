import os,sys
from src.entity.config_entity import TRANSFORMER_OBJECT_NAME,MODEL_FILE_NAME,TARGET_ENCODER_OBJECT_FILE_NAME
from glob import glob

class ModelResolver:
    def __init__(self,model_registry:str="saved_models",model_dir_name = 'model'):
        self.model_registry = model_registry
        os.makedirs(self.model_registry,exist_ok = True)
        self.model_dir_name = model_dir_name

    def get_latest_dir_path(self):
        try:
            dir_names = os.listdir(self.model_registry)
            if len(dir_names) == 0:
                return None
            
            dir_names = list(map(int,dir_names))
            latest_dir_name = max(dir_names)
            return os.path.join(self.model_registry,f"{latest_dir_name}")
        except Exception as e:
            raise e
    
    def get_latest_model_path():
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir == None:
                return Exception(f"Model not available")
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise e

    def get_latest_save_dir_path(self):
        try:
            latest_dir = get_latest_dir_path()
            if latest_dir == None:
                return os.path.join(self.model_registry,f"{0}")
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))
            return os.path.join(self.model_registry,f"{latest_dir_num+1}")
        except Exception as e:
            raise e
    
    def get_latest_save_model_path(self):
        try:
            latest_dir = get_latest_save_dir_path()
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise e

            