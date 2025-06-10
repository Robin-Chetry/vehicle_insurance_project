# === Importing Required Libraries ===

import sys                         # For accessing exception traceback info
import pandas as pd               # For handling tabular data using DataFrames
import numpy as np                # For handling missing values (np.nan)
from typing import Optional       # For specifying optional function parameters

# === Project-Specific Imports ===

from src.configuration.mongo_db_connection import MongoDBClient   # For MongoDB connection management
from src.constants import DATABASE_NAME                            # Constant for default database name
from src.exception import MyException                              # Custom exception class for robust error handling




# === Class Definition ===

class Proj1Data:
    """
    A utility class that connects to a MongoDB collection
    and exports its content as a pandas DataFrame.
    """

    def __init__(self) -> None:
        """
        Initializes a MongoDB client using the default database name.
        """
        try:
            # Create an instance of the MongoDB client
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)

        except Exception as e:
            # Raise custom exception with traceback info if connection fails
            raise MyException(e, sys)
        
        

    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Exports a MongoDB collection into a pandas DataFrame.

        Parameters:
        ----------
        collection_name : str
            The name of the MongoDB collection to export.

        database_name : Optional[str]
            Name of the database. If not provided, uses the default DATABASE_NAME.

        Returns:
        -------
        pd.DataFrame
            A cleaned DataFrame with '_id' column removed and 'na' values converted to np.nan.
        """
        try:
            # === Step 1: Access the collection ===
            if database_name is None:
                # Use the default database if no custom name is provided
                collection = self.mongo_client.database[collection_name]
            else:
                # Use a user-specified database
                collection = self.mongo_client[database_name][collection_name]

            # === Step 2: Fetch documents and load into DataFrame ===
            print("Fetching data from MongoDB...")
            df = pd.DataFrame(list(collection.find()))  # Convert all documents into a pandas DataFrame
            print(f"Data fetched with length: {len(df)}")

            # === Step 3: Drop 'id' column if present ===
            if "id" in df.columns.to_list():
                df = df.drop(columns=["id"], axis=1)

            # === Step 4: Replace all string "na" with actual NaN values ===
            df.replace({"na": np.nan}, inplace=True)

            # === Step 5: Return cleaned DataFrame ===
            return df

        except Exception as e:
            # Raise a custom exception with traceback if something goes wrong
            raise MyException(e, sys)
