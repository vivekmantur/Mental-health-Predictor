import os
from dotenv import load_dotenv

# ---------------------------------------------------------
# Load environment variables from .env file into the system
# ---------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------
# Fetch DATABASE_URL from environment variables
# This is used for DB connection (PostgreSQL/MySQL/etc.)
# ---------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")