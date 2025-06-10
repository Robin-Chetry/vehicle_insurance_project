import os  # To handle file paths and directories
import sys  # To pass system info to exception handler

from pandas import DataFrame  # To work with data as DataFrames
from sklearn.model_selection import train_test_split  # To split dataset into train/test

# Import your project's specific modules:
from src.entity.config_entity import DataIngestionConfig  # Config dataclass for ingestion settings
from src.entity.artifact_entity import DataIngestionArtifact  # Artifact dataclass for output info
from src.exception import MyException  # Custom exception class for consistent error handling
from src.logger import logging  # Custom logger for info/debug messages
from src.data_access.proj1_data import Proj1Data  # Class to interface with MongoDB data


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        """
        Initialize DataIngestion with configuration settings.

        Parameters:
        ----------
        data_ingestion_config: DataIngestionConfig
            Contains settings like collection name, file paths, and train-test split ratio.

        Purpose:
        --------
        Store the ingestion configuration in the class instance for later use.
        Wrap in try-except to catch config initialization errors.
        """
        try:
            self.data_ingestion_config = data_ingestion_config  # Save config
        except Exception as e:
            # If something goes wrong, raise a custom exception passing sys for traceback info
            raise MyException(e, sys)

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Export MongoDB collection data to a CSV file acting as feature store.

        Steps:
        ------
        1. Log start of export process.
        2. Use Proj1Data class to fetch collection data as DataFrame.
        3. Log shape of fetched data (rows, columns).
        4. Ensure the directory for the CSV file exists (create if not).
        5. Save the DataFrame as CSV to the specified feature store file path.
        6. Return the DataFrame for further processing.

        Raises:
        ------
        MyException if any step fails.
        """
        try:
            logging.info(f"Exporting data from mongodb")  # Log info for traceability

            # Create Proj1Data object to interact with MongoDB
            my_data = Proj1Data()

            # Call method to export entire collection as DataFrame
            dataframe = my_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
            )

            logging.info(f"Shape of dataframe: {dataframe.shape}")  # Log rows and cols count

            # Extract the configured path to save CSV file (feature store)
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            # Get directory path part from the file path
            dir_path = os.path.dirname(feature_store_file_path)

            # Make sure directory exists; if not, create it recursively
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")

            # Save DataFrame to CSV, excluding row indices, including header row
            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            return dataframe  # Return the data for use in later steps

        except Exception as e:
            # Wrap exceptions in custom error class with sys info for stack trace
            raise MyException(e, sys)

    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Split the given DataFrame into training and testing datasets, and save as CSV.

        Parameters:
        ----------
        dataframe : DataFrame
            The complete dataset to split into train and test.

        Process:
        --------
        1. Log entry into the method for debugging.
        2. Split DataFrame using sklearn's train_test_split with configured ratio.
        3. Log successful split.
        4. Ensure output directory for train/test files exists.
        5. Save train and test DataFrames to their respective CSV paths.
        6. Log completion and exit.

        Raises:
        ------
        MyException for any errors during split or file writing.
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            # Split data; test size taken from config, train is complementary
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")  # Log successful split

            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")

            # Get directory path of training file to ensure it exists before saving
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)  # Create directory if missing

            logging.info(f"Exporting train and test file path.")

            # Save train dataset CSV without index and with header
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)

            # Save test dataset CSV without index and with header
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info(f"Exported train and test file path.")  # Confirm save completion

        except Exception as e:
            # Raise exception with stack trace if splitting or saving fails
            raise MyException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Controls the end-to-end data ingestion pipeline.

        Steps:
        ------
        1. Export data from MongoDB collection into feature store CSV.
        2. Split this exported data into training and testing CSV files.
        3. Create and return a DataIngestionArtifact with file paths.

        Returns:
        --------
        DataIngestionArtifact
            Contains file paths of the saved training and testing CSV datasets.

        Raises:
        -------
        MyException for any error in export or split steps.
        """
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")

        try:
            # Export the full dataset from MongoDB into CSV and get DataFrame
            dataframe = self.export_data_into_feature_store()

            logging.info("Got the data from mongodb")  # Log fetch success

            # Split the full dataset into train/test CSV files
            self.split_data_as_train_test(dataframe)

            logging.info("Performed train test split on the dataset")  # Log split success

            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")

            # Prepare artifact with train and test CSV paths for downstream use
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")  # Log artifact details

            # Return artifact to next stage (like data validation)
            return data_ingestion_artifact

        except Exception as e:
            # Catch and raise any exception with full traceback
            raise MyException(e, sys) from e
