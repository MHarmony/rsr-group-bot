from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

host = getenv("DB_HOST")
port = getenv("DB_PORT")
username = getenv("DB_USERNAME")
password = getenv("DB_PASSWORD")
database = getenv("DB_NAME")

Engine = create_engine(
    f"postgresql://{username}:{password}@{host}:{port}/{database}",
    client_encoding="utf8",
)

Base = declarative_base()
