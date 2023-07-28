from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str
    feature_store_file_path: str 

@dataclass
class DataValidationArtifact:
    report_file_path:str

@dataclass
class DataTranformationArtifact:
    transformed_train_path:str
    transformed_test_path:str

@dataclass
class ModeltrainerArtifact:
    model_path:str 
    f1_training_score:float
    f1_test_score:float

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    improved_accuracy:float

@dataclass
class ModelPusherArtifact:...
