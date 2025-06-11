import os

import strawberry
from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from strawberry.fastapi import GraphQLRouter

from api.graphql.resolvers import Query, Mutation
from api.rest.users.views import user_router
from dependencies import context_dependency

MEDIA_DIR = "media"

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        title="My Application",
        description="This is a sample application using FastAPI.",
        version="1.0.0",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



    os.makedirs(MEDIA_DIR, exist_ok=True)

    api_v1_router = APIRouter(prefix="/v1/api")
    api_v1_router.include_router(user_router)
    app.include_router(api_v1_router)

    schema = strawberry.Schema(query=Query, mutation=Mutation)
    graphql_app = GraphQLRouter(
        schema, context_getter=context_dependency, multipart_uploads_enabled=True
    )

    app.include_router(graphql_app, prefix="/v1/graphql")

    app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

    return app