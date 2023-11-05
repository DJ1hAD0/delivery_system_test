import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_PORT = os.environ.get("DATABASE_PORT")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_HOSTNAME = os.environ.get("POSTGRES_HOSTNAME")


