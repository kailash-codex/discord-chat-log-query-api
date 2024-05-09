"""Reset the database by dropping all tables, creating tables, and inserting demo data."""

import sys
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import engine
from env import getenv
import entities

__authors__ = ["Kailash Muthu"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


if getenv("MODE") != "development":
    print("This script can only be run in development mode.", file=sys.stderr)
    print("Add MODE=development to your .env file in workspace's `backend/` directory")
    exit(1)


# Reset Tables
entities.EntityBase.metadata.drop_all(engine)

# Create Tables
entities.EntityBase.metadata.create_all(engine)