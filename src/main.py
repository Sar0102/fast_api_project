import strawberry
import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.staticfiles import StaticFiles
from strawberry.fastapi import GraphQLRouter

from api.graphql.resolvers import Query, Mutation
from api.rest.products.views import product_router
from api.rest.users.views import user_router
from dependencies import context_dependency

app = FastAPI()

api_v1_router = APIRouter(prefix="/v1/api")
api_v1_router.include_router(product_router)
api_v1_router.include_router(user_router)
app.include_router(api_v1_router)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(
    schema, context_getter=context_dependency, multipart_uploads_enabled=True
)

app.include_router(graphql_app, prefix="/v1/graphql")

app.mount("/media", StaticFiles(directory="media"), name="media")


if __name__ == "__main__":
    uvicorn.run(app=app, port=8010)
