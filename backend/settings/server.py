import os

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from src.routers import users

app = FastAPI(redoc_url=None)

origins = [
    "http://localhost",
    "http://localhost:3010",
    "http://frontend",
    "http://frontend:3010",
    os.environ.get('CORS_URL'),
    f"http://{os.environ.get('FRONT_APP_HOST')}:{str(os.environ.get('FRONT_APP_PORT'))}",
]
#
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Learn service",
        version="1.0.0",
        description="Learn service",
        routes=app.routes,
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi