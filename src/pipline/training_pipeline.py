# Importing system module for handling system-specific parameters and functions
import sys

# Importing custom exception class for consistent error handling
from src.exception import MyException

# Importing logging module for tracking pipeline execution
from src.logger import logging

# Importing all pipeline components that will be used in the training pipeline
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher

# Importing configuration classes for each pipeline stage
from src.entity.config_entity import (
    DataIngestionConfig,        # Configuration for data ingestion
    DataValidationConfig,       # Configuration for data validation
    DataTransformationConfig,   # Configuration for data transformation
    ModelTrainerConfig,         # Configuration for model training
    ModelEvaluationConfig,      # Configuration for model evaluation
    ModelPusherConfig           # Configuration for model deployment
)

# Importing artifact classes that hold outputs from each pipeline stage
from src.entity.artifact_entity import (
    DataIngestionArtifact,      # Output from data ingestion
    DataValidationArtifact,     # Output from data validation
    DataTransformationArtifact, # Output from data transformation
    ModelTrainerArtifact,       # Output from model training
    ModelEvaluationArtifact,    # Output from model evaluation
    ModelPusherArtifact        # Output from model deployment
)


class TrainPipeline:
    """
    Orchestrates the complete machine learning training pipeline from data ingestion to model deployment.
    Manages the sequential execution of all pipeline components.
    """

    def __init__(self):
        """
        Initializes the training pipeline by creating configuration objects for each stage.
        Each configuration contains parameters specific to that pipeline component.
        """
        # Initialize data ingestion configuration
        self.data_ingestion_config = DataIngestionConfig()
        
        # Initialize data validation configuration
        self.data_validation_config = DataValidationConfig()
        
        # Initialize data transformation configuration
        self.data_transformation_config = DataTransformationConfig()
        
        # Initialize model training configuration
        self.model_trainer_config = ModelTrainerConfig()
        
        # Initialize model evaluation configuration
        self.model_evaluation_config = ModelEvaluationConfig()
        
        # Initialize model deployment configuration
        self.model_pusher_config = ModelPusherConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        Executes the data ingestion component of the pipeline.
        Returns:
            DataIngestionArtifact: Contains paths to ingested data files and metadata
        """
        try:
            # Log entry into the method
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            
            # Log the data source being used
            logging.info("Getting the data from mongodb")
            
            # Create DataIngestion instance with configuration
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            
            # Execute data ingestion process and get results
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            
            # Log successful data retrieval
            logging.info("Got the train_set and test_set from mongodb")
            
            # Log exit from the method
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            
            # Return the data ingestion results
            return data_ingestion_artifact
        
        except Exception as e:
            # Convert any exceptions to custom exception format
            raise MyException(e, sys) from e
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        Executes the data validation component of the pipeline.
        Args:
            data_ingestion_artifact: Contains paths to the ingested data
        Returns:
            DataValidationArtifact: Contains validation results and reports
        """
        # Log entry into the method
        logging.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            # Create DataValidation instance with required artifacts and config
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )

            # Execute data validation process and get results
            data_validation_artifact = data_validation.initiate_data_validation()

            # Log successful validation
            logging.info("Performed the data validation operation")
            
            # Log exit from the method
            logging.info("Exited the start_data_validation method of TrainPipeline class")

            # Return the validation results
            return data_validation_artifact
        
        except Exception as e:
            # Convert any exceptions to custom exception format
            raise MyException(e, sys) from e
        
    def start_data_transformation(self, 
                                data_ingestion_artifact: DataIngestionArtifact, 
                                data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        """
        Executes the data transformation component of the pipeline.
        Args:
            data_ingestion_artifact: Contains paths to the ingested data
            data_validation_artifact: Contains validation results
        Returns:
            DataTransformationArtifact: Contains transformed datasets and preprocessing objects
        """
        try:
            # Create DataTransformation instance with required artifacts and config
            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_transformation_config=self.data_transformation_config,
                data_validation_artifact=data_validation_artifact
            )
            
            # Execute data transformation process and get results
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            
            # Return the transformation results
            return data_transformation_artifact
        
        except Exception as e:
            # Convert any exceptions to custom exception format
            raise MyException(e, sys)
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        """
        Executes the model training component of the pipeline.
        Args:
            data_transformation_artifact: Contains transformed training data
        Returns:
            ModelTrainerArtifact: Contains trained model and training metrics
        """
        try:
            # Create ModelTrainer instance with required artifacts and config
            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config
            )
            
            # Execute model training process and get results
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            
            # Return the training results
            return model_trainer_artifact

        except Exception as e:
            # Convert any exceptions to custom exception format
            raise MyException(e, sys)

    def start_model_evaluation(self, 
                             data_ingestion_artifact: DataIngestionArtifact,
                             model_trainer_artifact: ModelTrainerArtifact) -> ModelEvaluationArtifact:
        """
        Executes the model evaluation component of the pipeline.
        Args:
            data_ingestion_artifact: Contains reference to test data
            model_trainer_artifact: Contains trained model to evaluate
        Returns:
            ModelEvaluationArtifact: Contains evaluation metrics and acceptance status
        """
        try:
            # Create ModelEvaluation instance with required artifacts and config
            model_evaluation = ModelEvaluation(
                model_eval_config=self.model_evaluation_config,
                data_ingestion_artifact=data_ingestion_artifact,
                model_trainer_artifact=model_trainer_artifact
            )
            
            # Execute model evaluation process and get results
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            
            # Return the evaluation results
            return model_evaluation_artifact
        
        except Exception as e:
            # Convert any exceptions to custom exception format
            raise MyException(e, sys)

    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        """
        Executes the model deployment component of the pipeline.
        Args:
            model_evaluation_artifact: Contains evaluation results and approved model
        Returns:
            ModelPusherArtifact: Contains information about deployed model
        """
        try:
            # Create ModelPusher instance with required artifacts and config
            model_pusher = ModelPusher(
                model_evaluation_artifact=model_evaluation_artifact,
                model_pusher_config=self.model_pusher_config
            )
            
            # Execute model deployment process and get results
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            
            # Return the deployment results
            return model_pusher_artifact
        
        except Exception as e:
            # Convert any exceptions to custom exception format
            raise MyException(e, sys)

    def run_pipeline(self) -> None:
        """
        Executes the complete training pipeline in sequence.
        Handles the flow between components and manages the overall process.
        """
        try:
            # Log start of data ingestion and execute
            logging.info("Starting data ingestion...")
            data_ingestion_artifact = self.start_data_ingestion()
            
            # Log start of data validation and execute with ingestion results
            logging.info("Starting data validation...")
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )
            
            # Log start of data transformation and execute with previous results
            logging.info("Starting data transformation...")
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact, 
                data_validation_artifact=data_validation_artifact
            )
            
            # Log start of model training and execute with transformation results
            logging.info("Starting model training...")
            model_trainer_artifact = self.start_model_trainer(
                data_transformation_artifact=data_transformation_artifact
            )
            
            # Log start of model evaluation and execute with previous results
            logging.info("Starting model evaluation...")
            model_evaluation_artifact = self.start_model_evaluation(
                data_ingestion_artifact=data_ingestion_artifact,
                model_trainer_artifact=model_trainer_artifact
            )
            
            # Check if model was accepted in evaluation
            if not model_evaluation_artifact.is_model_accepted:
                # Log that model wasn't accepted and stop pipeline
                logging.info("Model not accepted. Stopping pipeline.")
                return None
                
            # Log start of model deployment and execute with evaluation results
            logging.info("Starting model pushing...")
            model_pusher_artifact = self.start_model_pusher(
                model_evaluation_artifact=model_evaluation_artifact
            )
            
            # Log successful pipeline completion
            logging.info("Pipeline completed successfully.")
            
        except Exception as e:
            # Log any errors during pipeline execution
            logging.error(f"Error in pipeline execution: {str(e)}")
            
            # Convert to custom exception format
            raise MyException(e, sys)