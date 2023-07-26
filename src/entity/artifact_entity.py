from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str
    feature_store_file_path: str 

@dataclass
class DataValidationArtifact:
    report_file_path:str

class DataTranformationArtifact:
    transformed_train_path:str
    transformed_test_path:str
class ModeltrainerArtifact:...

class ModelEvaluationArtifact:...

class ModelPusherArtifact:...
