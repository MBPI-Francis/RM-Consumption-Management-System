from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# This is the connection string (also known as a database URL) used to specify
# how to connect to your PostgreSQL database.
DATABASE_URL = "postgresql://postgresql:331212@localhost:5432/RMConsumptionDB"


# The engine is responsible for managing low-level details like connecting to
# the database and executing raw SQL commands.
engine = create_engine(DATABASE_URL)

# SssionLocal allows you to interact with the database in an organized and transactional way.
# Each request typically gets its own session instance.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Every model (table) in SQLAlchemy must extend this Base class.
# It provides SQLAlchemy with the metadata to map Python classes to database tables.
Base = declarative_base()
