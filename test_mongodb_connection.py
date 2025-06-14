#!/usr/bin/env python3
"""
Simple MongoDB connection test script
"""

from config import settings
from core.db.mongo import connection
from core.loggers_util import get_logger

logger = get_logger(__name__)


def test_mongodb_connection():
    """Test MongoDB connection and basic operations"""
    try:
        # Test connection
        logger.info("Testing MongoDB connection...")
        logger.info(f"Database host: {settings.MONGO_DATABASE_HOST}")
        logger.info(f"Database name: {settings.MONGO_DATABASE_NAME}")

        # Get database instance
        db = connection.get_database()
        logger.info(f"Successfully connected to database: {db.name}")

        # Test basic operation - list collections
        collections = db.list_collection_names()
        logger.info(f"Existing collections: {collections}")

        # Test document creation
        from core.db.documents import UserDocument

        # Create a test user
        test_user = UserDocument(first_name="Test", last_name="User")

        # Save the user
        user_id = test_user.save()
        logger.info(f"Created test user with ID: {user_id}")

        # Retrieve the user
        retrieved_user = UserDocument.find(first_name="Test", last_name="User")
        if retrieved_user:
            logger.info(
                f"Successfully retrieved user: {retrieved_user.first_name} {retrieved_user.last_name}"
            )
        else:
            logger.error("Failed to retrieve test user")

        logger.info("✅ MongoDB connection test PASSED!")
        return True

    except Exception as e:
        logger.error(f"❌ MongoDB connection test FAILED: {str(e)}")
        return False


if __name__ == "__main__":
    print("=== MongoDB Connection Test ===")
    print(f"MONGO_DATABASE_HOST from settings: {settings.MONGO_DATABASE_HOST}")
    print(f"MONGO_DATABASE_NAME from settings: {settings.MONGO_DATABASE_NAME}")
    print("=" * 40)
    test_mongodb_connection()
