from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from config import settings
from core.loggers_util import get_logger

logger = get_logger(__file__)


class MongoDatabaseConnector:
    """Singleton class to connect to MongoDB database."""

    _instance: MongoClient | None = None

    def __new__(cls, *args, **kwargs):
        """
        Args:
            cls: The class itself (MongoDatabaseConnector)
            *args: Variable positional arguments (not used in this implementation)
            **kwargs: Variable keyword arguments (not used in this implementation)

        Returns:
            MongoClient: The singleton instance of MongoDB client
        """
        # Check if a database instance already exists and if not, create a new one
        if cls._instance is None:
            try:
                cls._instance = MongoClient(settings.MONGO_DATABASE_HOST)
                logger.info(
                    f"Connection to database with uri: {settings.MONGO_DATABASE_HOST} successful"
                )
            except ConnectionFailure:
                logger.error(f"Couldn't connect to the database.")
                raise

        return cls._instance

    def get_database(self):
        assert self._instance, "Database connection not initialized"

        return self._instance[settings.MONGO_DATABASE_NAME]

    def close(self):
        if self._instance:
            self._instance.close()
            logger.info("Connected to database has been closed.")


connection = MongoDatabaseConnector()
