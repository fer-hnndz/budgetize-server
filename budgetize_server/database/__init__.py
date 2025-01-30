import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()

DB_NAME = os.environ.get("DB_NAME", "")
DB_HOST = os.environ.get("DB_HOST", "")
DB_USER = os.environ.get("DB_USER", "")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

IS_DEV = os.environ.get("DEV", False) == "True"
print("Dev Mode?", IS_DEV)
if IS_DEV:
    DB_NAME = "budgetize"
    DB_HOST = "localhost:8080"
    DB_USER = "postgres"
    DB_PASSWORD = "pass1234$"

URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

if IS_DEV:
    print("Connecting with URL", URL)

engine = create_engine(URL)
