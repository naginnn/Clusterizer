from sqlalchemy import Column, Integer, String, Boolean, BigInteger, ForeignKey, DateTime, Float, UUID
import uuid

from sqlalchemy.orm import relationship

from app_utils.models import BaseModel, Base

class AnswersData(BaseModel):

    __tablename__ = "answers_data"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, nullable=True)
    question = Column(String, nullable=True)
    answer = Column(String, nullable=True)
    count = Column(Integer, nullable=True)
    cluster = Column(String, nullable=True)
    sentiment = Column(String, nullable=True)
    context_cluster = Column(String, nullable=True)
    corrected = Column(String, nullable=True)

class Clusters(BaseModel):

    __tablename__ = "clusters"

    id = Column(Integer, primary_key=True)
    cluster = Column(Integer, nullable=True, unique=True)
    name = Column(String, nullable=True)