from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs

from events.models import AccessToken
from channels.db import database_sync_to_async

User = get_user_model()

class TokenAuthMiddleware:
    """
    This is a custom middleware that checks the request for a token in the query string and authenticates the user accordingly.
    """
    def __init__(self, app) -> None:
        self.app=app

    async def __call__(self, scope, recieve, send):
        query_string=scope.get("query_string", "b").decode()
        query_params=parse_qs(query_string)
        token=query_params.get('token', [None])[0]
        scope['user']=AnonymousUser()

        if token:
            try:
                user=await self.get_user_from_token(token)
                scope['user']=user
            except User.DoesNotExist:
                pass

        return await self.app(scope, recieve, send)
    @database_sync_to_async
    def get_user_from_token(self, token):
        return AccessToken.objects.select_related("user").get(key=token).user

def can_subscribe(user, channel: str):
    if channel.startswith('private_'):
        return user.is_staff
    return True

