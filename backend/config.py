import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
STORAGE_PATH = os.getenv("STORAGE_PATH", "storage/")  # Local storage folder
