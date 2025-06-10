# Standard library imports
import os            # For accessing environment variables (e.g., MongoDB connection string)
import sys           # For capturing exception information (used in custom exceptions)

# External libraries
import pymongo       # PyMongo is the official MongoDB driver for Python
import certifi       # Provides SSL certificates to securely connect to MongoDB

# Project-specific imports
from src.exception import MyException     # Custom exception class to wrap and handle exceptions uniformly
from src.logger import logging            # Custom logger to write logs (info, warnings, errors)
from src.constants import DATABASE_NAME, MONGODB_URL_KEY  # Constants defined for DB name and MongoDB URL env key



# Load certificate authority file for TLS (secure connection to MongoDB)
ca = certifi.where()

class MongoDBClient:
    """
    MongoDBClient handles the connection to a MongoDB database.

    Attributes:
    ----------
    client : pymongo.MongoClient
        A shared MongoClient used by all instances of MongoDBClient to avoid redundant connections.

    database : pymongo.database.Database
        A specific MongoDB database instance that this class connects to.
    """

    # Class-level attribute to store a shared MongoClient instance
    client = None
    
    
    

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        """
        Constructor that initializes a MongoDB connection using the provided database name.

        Parameters:
        ----------
        database_name : str, optional
            The name of the MongoDB database to connect to (default is from constants.py)

        Raises:
        ------
        MyException
            If the connection fails or environment variable for MongoDB URL is not set.
        """
        try:
            # If no shared MongoClient exists yet, create a new connection
            if MongoDBClient.client is None:
                # Get MongoDB URL from environment variables
                mongo_db_url = os.getenv(MONGODB_URL_KEY)

                # Raise an error if the URL is not found in environment
                if mongo_db_url is None:
                    raise Exception(f"Environment variable '{MONGODB_URL_KEY}' is not set.")

                # Create a secure MongoClient using SSL certificate from certifi
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

            # Set instance variables from the class-level client
            self.client = MongoDBClient.client  # Reuse the already established connection
            self.database = self.client[database_name]  # Access the specified database
            self.database_name = database_name          # Store database name for reference

            # Log a successful connection
            logging.info("MongoDB connection successful.")

        except Exception as e:
            # Raise a custom exception with system traceback information
            raise MyException(e, sys)
