# divineshop/db.py
from mongoengine import connect
from dotenv import load_dotenv
import os

load_dotenv()


# Initialize the MongoDB client here, so it's shared across modules
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv("DB_NAME")
try:
    # Attempt to establish a connection to the MongoDB database
    result = connect(DB_NAME, host=DB_HOST)
    print("Successfully connected to the MongoDB database!", result)
except Exception as e:
    print(f"Failed to connect to the MongoDB database: {e}")
