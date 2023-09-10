from typing import Any, AsyncIterator, List, Optional, Annotated

from fastapi import Query
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field


from src.models import AnswersData


class AnswerDataFilter(Filter):
    """ Фильтры поиска объектов """

    question__ilike: Optional[str] = Field(Query(None, description="Вопрос"), alias="question")
    question_id__in: Optional[list[int]] = Field(Query(None, description="id вопроса"), alias="question_id")
    answer__ilike: Optional[str] = Field(Query(None, description="Ответ"), alias="answer")
    count__in: Optional[list[int]] = Field(Query(None, description="Количество ответов (совп.)"), alias="count")
    cluster__ilike: Optional[str] = Field(Query(None, description="Кластер"), alias="cluster")
    sentiment__ilike: Optional[str] = Field(Query(None, description="Сантименты"), alias="sentiment")
    context_cluster__ilike: Optional[str] = Field(Query(None, description="Контекст кластера"), alias="context_cluster")
    corrected__ilike: Optional[str] = Field(Query(None, description="Корректировка"), alias="corrected")

    class Constants(Filter.Constants):
        model = AnswersData

    class Config:
        allow_population_by_field_name = True