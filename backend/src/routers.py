from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from settings.database import get_session
from src.filters import AnswerDataFilter
from src.models import AnswersData
from fastapi_filter import FilterDepends
from src.schemas import Question
from src.service.model import predict

users = APIRouter()

@users.post("/upload_data", status_code=200)
async def upload_data(question: Question, session: AsyncSession = Depends(get_session)):
    try:
        response = predict(question.dict())
        if response:
            return JSONResponse({'result': response})
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)

@users.get("/load_data", status_code=200)
async def upload_data(questions_filter: AnswerDataFilter = FilterDepends(AnswerDataFilter), session: AsyncSession = Depends(get_session)):
    query = questions_filter.filter(select(AnswersData))
    result = await session.execute(query)
    questions = result.scalars().all()
    if questions:
        return {'questions': questions}
    raise HTTPException(status_code=404, detail="Question not found")








