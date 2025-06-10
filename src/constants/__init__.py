import os  # Used for interacting with the operating system (e.g., file paths)
from datetime import date  # To get the current date, here used to fetch current year





# ----------------------------- MongoDB Configuration -----------------------------
DATABASE_NAME = "Proj1"  # MongoDB database name
COLLECTION_NAME = "Proj1-Data"  # MongoDB collection name inside the database
MONGODB_URL_KEY = "MONGODB_URL"  # Environment variable key to fetch the MongoDB URL




# ----------------------------- General Pipeline Settings -----------------------------
PIPELINE_NAME: str = ""  # Optional name for the ML pipeline (can be used for tracking versions)
ARTIFACT_DIR: str = "artifact"  # Directory to store all pipeline artifacts like models, data, etc.




# ----------------------------- File Names for Model & Data -----------------------------
MODEL_FILE_NAME = "model.pkl"  # Pickle file name where the trained model will be saved
TARGET_COLUMN = "Response"  # Name of the target column in the dataset (used for training)
CURRENT_YEAR = date.today().year  # Dynamically fetches the current year (e.g., 2025)
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"  # File name for saving preprocessing pipeline (e.g., scalers)

FILE_NAME: str = "data.csv"  # Main data file name (raw input)
TRAIN_FILE_NAME: str = "train.csv"  # File name to store training dataset
TEST_FILE_NAME: str = "test.csv"  # File name to store testing dataset
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")  # Path to schema definition file




# ----------------------------- AWS Configuration -----------------------------
AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"  # Environment variable key for AWS access key ID
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"  # Environment variable key for AWS secret key
REGION_NAME = "us-east-1"  # AWS region where resources (like S3 bucket) are hosted



# ----------------------------- Data Ingestion Constants -----------------------------
DATA_INGESTION_COLLECTION_NAME: str = "Proj1-Data"  # MongoDB collection name used in data ingestion
DATA_INGESTION_DIR_NAME: str = "data_ingestion"  # Directory for storing ingestion-related files
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"  # Directory to store feature store data
DATA_INGESTION_INGESTED_DIR: str = "ingested"  # Directory to store split ingested train/test data
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.25  # Ratio to split data into test (25%) and train (75%)




# ----------------------------- Data Validation Constants -----------------------------
DATA_VALIDATION_DIR_NAME: str = "data_validation"  # Directory to store data validation artifacts
DATA_VALIDATION_REPORT_FILE_NAME: str = "report.yaml"  # File name for storing data validation report (e.g., schema mismatch, missing values)





# ----------------------------- Data Transformation Constants -----------------------------
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"  # Directory to store transformation-related outputs
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"  # Directory for transformed train/test datasets
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"  # Directory for storing transformation objects (like encoders, scalers)




# ----------------------------- Model Trainer Constants -----------------------------
MODEL_TRAINER_DIR_NAME: str = "model_trainer"  # Directory for storing model training files
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"  # Directory where the final trained model will be saved
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"  # Name of the final trained model file
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6  # Minimum accuracy/R² required for accepting the model
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")  # Path to model configuration file (e.g., algorithm, hyperparameters)





# Hyperparameters for training (likely for Random Forest or Decision Tree)
MODEL_TRAINER_N_ESTIMATORS = 200  # Number of trees in the forest
MODEL_TRAINER_MIN_SAMPLES_SPLIT: int = 7  # Minimum number of samples to split an internal node
MODEL_TRAINER_MIN_SAMPLES_LEAF: int = 6  # Minimum number of samples required to be at a leaf node
MIN_SAMPLES_SPLIT_MAX_DEPTH: int = 10  # Maximum depth of the tree
MIN_SAMPLES_SPLIT_CRITERION: str = 'entropy'  # Criterion for information gain (e.g., 'gini' or 'entropy')
MIN_SAMPLES_SPLIT_RANDOM_STATE: int = 101  # Random state to ensure reproducibility





# ----------------------------- Model Evaluation & Deployment -----------------------------
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02  # Minimum change in score to consider retraining/deploying new model
MODEL_BUCKET_NAME = "my-model-mlopsproj"  # S3 bucket name for storing model artifacts
MODEL_PUSHER_S3_KEY = "model-registry"  # S3 folder/key prefix for model registry




# ----------------------------- Application Hosting -----------------------------
APP_HOST = "0.0.0.0"  # Host to run the Flask/FastAPI server (0.0.0.0 allows access from any IP, useful in Docker)
APP_PORT = 5000  # Port on which the app will run (standard for Flask development servers)
