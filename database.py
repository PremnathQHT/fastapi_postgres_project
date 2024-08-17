from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Link to connect postgres DB
URL_DATABASE = 'postgresql://postgres:coderprem@localhost:5432/python_db'

#Gatekeeper of the Database
engine = create_engine(URL_DATABASE)

#Session Maker (Workspace provider)
SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Blueprint of the Databases
Base = declarative_base()