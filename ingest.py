import time
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils import ingest_data

# Database connection details

DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@localhost:5432/gold_standard"

engine = create_engine(DATABASE_URL, echo=True)

# Define database table schema
Base = declarative_base()


# Create all tables in the engine (if they don't exist)
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
session = Session()

# Loop through pages until there are no more projects
page_number = 1
while True:
    ingest_data(page_number, session)
    time.sleep(2)  # Throttle requests by waiting for 2 seconds between requests to prevent hitting server too quickly
    page_number += 1

print('Web Scraping Gold Standard Registry Website completed')
