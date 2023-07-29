from src.logger import logging
from src.exception import SrcException
import os,sys
from src import utility
from src.predictor import ModelResolver
from datetime import datetime
PREDICTION_DIR = "prediction"
import pandas as pd 
import numpy as np
from src.config import TARGET_COLUMN


def start_batch_prediction(input_file_path):
    try:
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        logging.info(f"creating model resolver object")
        model_resolver= ModelResolver()
        logging.info(f"reading input file : {input_file_path}")
        df = pd.read_csv(input_file_path)

        logging.info(f"loading transformer to transform the dataset")

        logging.info(f"loading model to makee predictions")
        model = utility.load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(df.drop(TARGET_COLUMN,axis=1))

        df['prediction'] = prediction

        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")

        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)
        df.to_csv(prediction_file_path,index=False,header=True)
        return prediction_file_path
    except Exception as e:
        raise SrcException(e,sys)
