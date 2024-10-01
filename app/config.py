
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
__desc__ = "Configuration File of the Program"


#Import
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False") == "True"

SECRET_KEY = os.getenv("SECRET_KEY")

#DB info
DATABASE_TYPE=os.getenv("DATABASE_TYPE")
DATABASE_USER=os.getenv("DATABASE_USER")
DATABASE_PASSWORD=os.getenv("DATABASE_PASSWORD")
DATABASE_HOST=os.getenv("DATABASE_HOST")
DATABASE_PORT=os.getenv("DATABASE_PORT")
DATABASE_NAME=os.getenv("DATABASE_NAME")


# Email info
EMAIL_HOST=os.getenv("EMAIL_HOST")
EMAIL_PORT=os.getenv("EMAIL_PORT")
EMAIL_USER=os.getenv("EMAIL_USER")
EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")

#Host info
HOST=os.getenv("HOST")

# Port info
PORT=os.getenv("PORT")



#Log information
LOGFILE=os.getenv("LOGFILE")
MODE=os.getenv("MODE")
LOGPATH=os.getenv("LOGPATH")
