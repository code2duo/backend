from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from firebase_admin import auth

from authentication.scripts import generate_username

User = get_user_model()


class FirebaseAuthenticationMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    uid_field = User.UID_FIELD

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        if scope.get("user"):
            return await self.inner(scope, receive, send)
        firebase_token = parse_qs(scope["query_string"].decode())["token"][0]
        try:
            payload = auth.verify_id_token(firebase_token)
            if (
                payload["firebase"]["sign_in_provider"] == "anonymous"
                or not payload["email_verified"]
            ):
                raise TypeError
            uid = payload["uid"]
        except (
            ValueError,
            TypeError,
            auth.ExpiredIdTokenError,
            auth.InvalidIdTokenError,
            auth.RevokedIdTokenError,
        ):
            scope["user"] = AnonymousUser()
            return await self.inner(scope, receive, send)

        scope["user"] = await self.get_or_create(uid)
        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_or_create(self, uid) -> User:
        """
        Returns an user that matches the payload's user uid and email.
        """

        try:
            user = User.objects.get(**{self.uid_field: uid})
        except User.DoesNotExist:
            firebase_user: auth.UserRecord = auth.get_user(uid)
            fields = {
                self.uid_field: uid,
                "email": firebase_user.email,
                "username": generate_username(firebase_user.email),
            }
            user = User.objects.create(**fields)

        return user


def FirebaseAuthenticationMiddlewareStack(inner):
    return FirebaseAuthenticationMiddleware(inner)
