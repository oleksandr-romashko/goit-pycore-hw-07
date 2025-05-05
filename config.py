from dotenv import load_dotenv
import os

# Load environment variables from .env file if present
load_dotenv()

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
