from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base
import psycopg2

# This is the connection string (also known as a database URL) used to specify
# How to connect to your PostgreSQL database.
DATABASE_URL = "postgresql://postgres:mbpi@192.168.1.13:5432/RMDummyDB"
# DATABASE_URL = "postgresql://postgres:331212@localhost:5432/RMManagementSystemDB"


# The engine is responsible for managing low-level details like connecting to
# the database and executing raw SQL commands.
engine = create_engine(DATABASE_URL)

# SssionLocal allows you to interact with the database in an organized and transactional way.
# Each request typically gets its own session instance.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Every model (table) in SQLAlchemy must extend this Base class.
# It provides SQLAlchemy with the metadata to map Python classes to database tables.
Base = declarative_base()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


server_ip = "http://127.0.0.1:8000"

