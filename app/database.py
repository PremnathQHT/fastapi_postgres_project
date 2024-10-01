"""
Private License (toolsmgt)

This script is privately licensed and confidential. It is not intended for
public distribution or use without explicit permission from the owner.

All rights reserved (c) 2024.
"""

__author__ = "Premnath Palanichamy"
__copyright__ = "Copyright 2024, toolsmgt"
__license__ = "Refer Terms and Conditions"
__version__ = "1.0"
__maintainer__ = "Premnath"
__email__ = "premnath@quehive.com"
__status__ = "Development"
__desc__ = "Main Program of toolsmgt applications"

#Import
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import DATABASE_HOST,DATABASE_NAME,DATABASE_PASSWORD,DATABASE_PORT,DATABASE_TYPE,DATABASE_USER
import app.toolsmgtlogger as qtslogger

# Create logger object
logger = qtslogger.logger()

#Link to connect postgres DB

# Function to check and create database
def check_and_create_db():
    # Connect to PostgreSQL server
    conn = psycopg2.connect(
        dbname='postgres',  # Default database to connect to before creating the new one
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Check if the database exists
    cursor.execute(
        sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s;"),
        [DATABASE_NAME]
    )
    exists = cursor.fetchone()

    if not exists:
        # Create the database if it doesn't exist
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DATABASE_NAME)
            )
        )
    #     logger.info(f"Database '{DATABASE_NAME}' created successfully.")
    # else:
    #     logger.info(f"Database '{DATABASE_NAME}' already exists.")

    cursor.close()
    conn.close()

# Call the function before creating engine
check_and_create_db()







#DATABASE_URL=postgresql://postgres:coderprem@localhost:5432/python_db
URL_DATABASE =f"{DATABASE_TYPE}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


#Gatekeeper of the Database
engine = create_engine(URL_DATABASE,pool_size=10, max_overflow=20)

#Session Maker (Workspace provider)
SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Blueprint of the Databases
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        