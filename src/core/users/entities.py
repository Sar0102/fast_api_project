from core.permissions import Permissions


class BaseUser:
    def __init__(
        self,
        username: str,
        password: str,
        email: str,
        is_admin: bool,
        permissions: list[str] | None = None,
    ) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin
        self.permissions = permissions


class AdminUser(BaseUser):
    def __init__(self, username: str, password: str, email: str) -> None:
        super().__init__(username, password, email, is_admin=True, permissions=Permissions.list())


class RegularUser(BaseUser):
    def __init__(
        self, username: str, password: str, email: str, permissions: list[str] | None = None
    ) -> None:
        super().__init__(username, password, email, is_admin=False, permissions=permissions)
