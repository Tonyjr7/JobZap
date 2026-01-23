from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from settings import Settings

# Fetch variables
USER = Settings().user
PASSWORD = Settings().password
HOST = Settings().host
PORT = Settings().port
DBNAME = Settings().dbname


# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
"""
The engine manages the connection to the database and handles query execution.
"""
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    engine.connect()
    print("DB connected")
except OperationalError as e:
    print("DB connection failed:", e)


# Database dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()