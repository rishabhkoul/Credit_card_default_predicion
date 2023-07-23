from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str
    feature_store_file_path: str 

class DataValidationArtifact:...

class DataTranformationArtifact:...

class ModeltrainerArtifact:...

class ModelEvaluationArtifact:...

class ModelPusherArtifact:...
