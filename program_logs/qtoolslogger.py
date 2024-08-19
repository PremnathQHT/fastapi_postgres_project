import logging
import os

# Get the current directory of this script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Set the logs directory relative to the current directory
log_directory = os.path.join(current_directory, "logs")
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_directory, "app.log")),
        logging.StreamHandler()
    ]
)

# Optionally, create a logger instance
logger = logging.getLogger(__name__)
