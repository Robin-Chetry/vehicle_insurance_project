from dataclasses import dataclass

# ===============================================================
# Artifact generated after Data Ingestion
# ===============================================================

@dataclass
class DataIngestionArtifact:
    """
    Stores file paths for training and testing data generated during data ingestion.
    """
    trained_file_path: str  # Path to the training dataset after split
    test_file_path: str     # Path to the testing dataset after split

# ===============================================================
# Artifact generated after Data Validation
# ===============================================================

@dataclass
class DataValidationArtifact:
    """
    Stores the results of data validation.
    """
    validation_status: bool                   # Whether data passed validation checks
    message: str                              # Optional message about success/failure
    validation_report_file_path: str          # Path to the YAML/JSON report summarizing validation

# ===============================================================
# Artifact generated after Data Transformation
# ===============================================================

@dataclass
class DataTransformationArtifact:
    """
    Stores transformed datasets and preprocessing object used during transformation.
    """
    transformed_object_file_path: str         # Path to the saved preprocessor (e.g., scaler, encoder)
    transformed_train_file_path: str          # Path to the transformed training data (usually .npy format)
    transformed_test_file_path: str           # Path to the transformed testing data

# ===============================================================
# Metrics related to Model Evaluation
# ===============================================================

@dataclass
class ClassificationMetricArtifact:
    """
    Stores key classification performance metrics of the model.
    """
    f1_score: float                           # Harmonic mean of precision and recall
    precision_score: float                    # Precision score of the model
    recall_score: float                       # Recall score of the model

# ===============================================================
# Artifact generated after Model Training
# ===============================================================

@dataclass
class ModelTrainerArtifact:
    """
    Stores the trained model's path and associated performance metrics.
    """
    trained_model_file_path: str              # Path where the trained model is saved (.pkl file)
    metric_artifact: ClassificationMetricArtifact  # Performance metrics object for the model

# ===============================================================
# Artifact generated after Model Evaluation (Comparison with previous model)
# ===============================================================

@dataclass
class ModelEvaluationArtifact:
    """
    Stores evaluation results of the trained model against existing models.
    """
    is_model_accepted: bool                   # Indicates whether the new model was accepted for deployment
    changed_accuracy: float                   # Difference in accuracy between new and old model
    s3_model_path: str                        # Path to the model stored in cloud (S3, GCP, etc.)
    trained_model_path: str                   # Local path to the newly trained model

# ===============================================================
# Artifact generated after Model Pusher (Deployment phase)
# ===============================================================

@dataclass
class ModelPusherArtifact:
    """
    Stores information about the model's deployment to a remote location like S3.
    """
    bucket_name: str                          # Name of the bucket where the model is pushed
    s3_model_path: str                        # Path in the bucket where model is stored
