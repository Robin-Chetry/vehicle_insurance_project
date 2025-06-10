# Import standard libraries
import os
from datetime import datetime
from dataclasses import dataclass

# Import constant variables defined elsewhere in your project
from src.constants import *

# Generate a timestamp string used for uniquely naming artifact directories
TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

# ========================================================================================
# PIPELINE CONFIGURATION
# ========================================================================================

@dataclass
class TrainingPipelineConfig:
    """
    Configuration for the overall training pipeline.
    Stores basic identifiers like pipeline name and artifact directory.
    """
    pipeline_name: str = PIPELINE_NAME
    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)
    timestamp: str = TIMESTAMP

# Initialize the pipeline config object
training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()

# ========================================================================================
# DATA INGESTION CONFIGURATION
# ========================================================================================

@dataclass
class DataIngestionConfig:
    """
    Configuration for data ingestion stage.
    Defines paths for storing raw data and split data.
    """
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
    feature_store_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
    training_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
    testing_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection_name: str = DATA_INGESTION_COLLECTION_NAME

# ========================================================================================
# DATA VALIDATION CONFIGURATION
# ========================================================================================

@dataclass
class DataValidationConfig:
    """
    Configuration for data validation stage.
    Defines where validation reports will be saved.
    """
    data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)
    validation_report_file_path: str = os.path.join(data_validation_dir, DATA_VALIDATION_REPORT_FILE_NAME)

# ========================================================================================
# DATA TRANSFORMATION CONFIGURATION
# ========================================================================================

@dataclass
class DataTransformationConfig:
    """
    Configuration for data transformation stage.
    Specifies paths to transformed training/testing data and transformation objects.
    """
    data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME)
    transformed_train_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        TRAIN_FILE_NAME.replace("csv", "npy")
    )
    transformed_test_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        TEST_FILE_NAME.replace("csv", "npy")
    )
    transformed_object_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
        PREPROCSSING_OBJECT_FILE_NAME
    )

# ========================================================================================
# MODEL TRAINER CONFIGURATION
# ========================================================================================

@dataclass
class ModelTrainerConfig:
    """
    Configuration for model training stage.
    Specifies model storage, training hyperparameters, and model config path.
    """
    model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME)
    trained_model_file_path: str = os.path.join(
        model_trainer_dir,
        MODEL_TRAINER_TRAINED_MODEL_DIR,
        MODEL_FILE_NAME
    )
    expected_accuracy: float = MODEL_TRAINER_EXPECTED_SCORE
    model_config_file_path: str = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH

    # Additional hyperparameters for model training
    _n_estimators = MODEL_TRAINER_N_ESTIMATORS
    _min_samples_split = MODEL_TRAINER_MIN_SAMPLES_SPLIT
    _min_samples_leaf = MODEL_TRAINER_MIN_SAMPLES_LEAF
    _max_depth = MIN_SAMPLES_SPLIT_MAX_DEPTH
    _criterion = MIN_SAMPLES_SPLIT_CRITERION
    _random_state = MIN_SAMPLES_SPLIT_RANDOM_STATE

# ========================================================================================
# MODEL EVALUATION CONFIGURATION
# ========================================================================================

@dataclass
class ModelEvaluationConfig:
    """
    Configuration for model evaluation stage.
    Used to compare new model performance with previous models.
    """
    changed_threshold_score: float = MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE
    bucket_name: str = MODEL_BUCKET_NAME
    s3_model_key_path: str = MODEL_FILE_NAME

# ========================================================================================
# MODEL PUSHER CONFIGURATION
# ========================================================================================

@dataclass
class ModelPusherConfig:
    """
    Configuration for model deployment (pushing to S3 or model registry).
    """
    bucket_name: str = MODEL_BUCKET_NAME
    s3_model_key_path: str = MODEL_FILE_NAME

# ========================================================================================
# VEHICLE PREDICTION CONFIGURATION (for inference use case)
# ========================================================================================

@dataclass
class VehiclePredictorConfig:
    """
    Configuration for loading model from S3 or local storage for making predictions.
    """
    model_file_path: str = MODEL_FILE_NAME
    model_bucket_name: str = MODEL_BUCKET_NAME
