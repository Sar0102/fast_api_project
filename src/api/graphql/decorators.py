from functools import wraps

from api.graphql.users.schemas import UserPage


def require_authentication(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        info = kwargs.get("info") or args[1]
        current_user = info.context.get("current_user")
        if not current_user:
            raise ValueError("Authentication required!")
        return await func(*args, **kwargs)

    return wrapper


def paginate(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        limit = kwargs.get("limit", 10)
        offset = kwargs.get("offset", 0)
        all_items = await func(*args, **kwargs)
        total_items = len(all_items)
        paginated_items = list(all_items)[offset : offset + limit]
        return UserPage(items=paginated_items, total=total_items, offset=offset, limit=limit)

    return wrapper
