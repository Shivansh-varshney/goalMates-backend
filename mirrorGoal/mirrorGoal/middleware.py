import jwt
from django.conf import settings
from channels.db import database_sync_to_async

@database_sync_to_async
def get_user(token):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return User.objects.get(id=payload["user_id"])
    except Exception:
        return None

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        token = None

        if query_string:
            try:
                params = dict(q.split("=") for q in query_string.split("&"))
                token = params.get("token")
            except Exception:
                pass

        scope["user"] = await get_user(token) if token else None
        return await self.inner(scope, receive, send)
