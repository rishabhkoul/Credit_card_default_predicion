from src.logger import logging
from src.exception import SrcException
from src.entity import config_entity,artifact_entity
import os,sys
from sklearn.ensemble import AdaBoostClasifier
from sklearn.metrics import f1_score
from src import utility


class ModelTrainer:
    def __init__(self,model_trainer_config:config_entity.ModeltrainerConfig,data_transformation_artifact:artifact_entity.DataTranformationArtifact):
        try:
            logging.info(f"{'>'*20} Model Trainer {'<'*20} ")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise SrcException(e,sys)

    def train_model(x,y):
        try:
            ada = AdaBoostClasifier()
            ada.fit(x,y)
            return ada
        except Exception as e:
            raise SrcException(e,sys)

    def initiate_model_trainer(self):
        try:
            logging.info(f"Loading training and testing arrays")
            train_arr = utility.load_numpy_array_data(file_path= self.data_transformation_artifact.transformed_train_path)
            test_arr = utility.load_numpy_array_data(file_path = self.data_transformation_artifact.transformed_test_path)

            logging.info("Splitting the data into input features and target feature from both train and test arrays")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            X_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            logging.info("Training the model")
            model = train_model(x_train,y_train)

            logging.info("Calculating the F1 score for train data")
            y_hat_train = model.predict(x_train)
            f1_train_score = f1_score(y_true=y_train,y_pred=y_hat_train)

            logging.info("calculating the F1 score for test data")
            y_hat_test = mmodel.predict(x_test)
            f1_test_score = f1_score(y_true=y_test,y_pred=y_hat_test)

            logging.info(f"Train Score: {f1_train_score} and test score {f1_test_score}")

            logging.info("Checking if model is underfitting or not")
            if f1_test_score < self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is unable to give excpeced accuracy: {self.model_trainer_config.expected_score} actual model score: {f1_test_score}")

            diff = abs(f1_train_score - f1_test_score)
            logging.info(f"Checkin if the model is overfitting or not")
            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score differece: {diff} is higher than the overfitting threshold {self.model_trainer_config.overfitting_threshold}")

            logging.info("Saving model object")
            utility.save_object(self.model_trainer_config.model_path, model)

            #prepare artifact
            logging.info(f"pepaing model trainer artifact")
            model_trainer_artifact = artifact_entity.ModeltrainerArtifact(model_path=self.model_trainer_config.model_path, f1_training_score=f1_train_score, f1_test_score=f1_test_score)
            logging.info(f"model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact
 
        except Exception as e:
            raise SrcException(e,sys)