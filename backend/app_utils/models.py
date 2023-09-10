import uuid
from datetime import timedelta, datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.collections import InstrumentedList

Base = declarative_base()

class BaseModel(Base):

    __abstract__ = True

    def to_dict(self, rel=True, ignored_fields=(), **additional_fields):
        attrs = {} or additional_fields
        for attribute, value in self.__dict__.items():
            if attribute in ignored_fields:
                continue
            if not attribute.startswith('_'):
                if isinstance(value, InstrumentedList):
                    if rel:
                        attrs[attribute] = []
                        for val in value:
                            attrs[attribute].append(val.to_dict(rel, ignored_fields))
                        continue
                    else:
                        continue
                if isinstance(value, uuid.UUID):
                    attrs[attribute] = str(value)
                elif isinstance(value, datetime):
                    val = value + timedelta(hours=3)
                    attrs[attribute] = val.strftime("%Y/%m/%d, %H:%M")
                else:
                    attrs[attribute] = value
        return attrs