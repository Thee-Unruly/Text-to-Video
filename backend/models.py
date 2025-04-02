from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GeneratedVideo(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
