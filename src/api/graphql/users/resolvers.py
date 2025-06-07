from datetime import timedelta

import strawberry
from strawberry import Info
from strawberry.file_uploads import Upload

from api.graphql.decorators import require_authentication, paginate
from api.graphql.users.schemas import User, Token, UserPage
from core.users.dto import UserCreateDTO
from core.users.services import (
    ACCESS_TOKEN_EXPIRES_MINUTES,
    REFRESH_TOKEN_EXPIRES_MINUTES,
    UserService,
)
from infrastructure.database.uow import UnitOfWork


@strawberry.type
class FileMutation:
    @strawberry.mutation
    async def upload_file(self, file: Upload) -> str:
        content = await file.read()
        filename = file.filename
        with open(f"media/{filename}", "wb") as f:
            f.write(content)
        return f"File {filename} uploaded successfully."


@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def register(
        self,
        info: Info,
        username: str,
        password: str,
        email: str,
    ) -> User:
        uow: UnitOfWork = info.context["uow"]

        await UserService.add(
            uow=uow,
            create_dto=UserCreateDTO(
                username=username,
                password=password,
                email=email,
                is_admin=False,
                permissions=None,
            ),
        )
        return User(username=username, email=email)

    @strawberry.mutation
    async def login(self, info: Info, username: str, password: str) -> Token:
        uow: UnitOfWork = info.context["uow"]
        user = await UserService.authenticate_user(uow, username, password)
        if not user:
            raise ValueError("Incorrect password or username")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
        refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRES_MINUTES)
        access_token = UserService.create_token(
            data={"sub": username, "type": "access"}, expires_delta=access_token_expires
        )
        refresh_token = UserService.create_token(
            data={"sub": username, "type": "refresh"}, expires_delta=refresh_token_expires
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )


@strawberry.type
class UserQuery:
    @strawberry.field
    async def all_users(self, info: Info, limit: int, offset: int) -> UserPage:
        uow: UnitOfWork = info.context["uow"]

        all_items = await UserService.get_all(uow)
        total_items = len(all_items)
        paginated_items = list(all_items)[offset : offset + limit]
        return UserPage(items=paginated_items, total=total_items, offset=offset, limit=limit)
