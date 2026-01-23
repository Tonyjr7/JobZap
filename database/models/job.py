from database.base import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class Job(Base):
    """"SQLAlchemy model for the Job table."""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_title = Column(String)
    company = Column(String, index=True)
    job_url = Column(String)
    date_added = Column(DateTime, server_default=func.now())
