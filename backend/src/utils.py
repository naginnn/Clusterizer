import hashlib
import random
import string
from datetime import datetime, timedelta
import jwt
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession




#


# async def check_role(username: str, app_role: str, session: AsyncSession):
    # query = select(User).filter(username == User.username)
    # user = (await session.execute(query)).scalars().one()
    # if user:
    #     roles = [role.role for role in user.roles]
    #     if app_role:
    #         return app_role in roles
    # return True
