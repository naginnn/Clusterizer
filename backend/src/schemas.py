from fastapi import Query
from pydantic import BaseModel, EmailStr

from typing import Optional
from pydantic import UUID4, BaseModel, EmailStr, Field, validator
from pydantic.validators import datetime




class Answer(BaseModel):
    answer: str
    count: int

class Question(BaseModel):
    id: int
    question: str
    answers: list[Answer]

