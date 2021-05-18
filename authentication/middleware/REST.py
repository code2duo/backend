from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from firebase_admin import auth

from authentication.scripts import generate_username

User = get_user_model()


class BaseFirebaseAuthentication(BaseAuthentication):
    """
    Base implementation of token based authentication using firebase.
    """

    auth_header_prefix = "Bearer"
    uid_field = User.UID_FIELD

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and decoded firebase payload if a valid signature
        has been supplied. Otherwise returns `None`.
        """
        firebase_token = self.get_token(request)

        if not firebase_token:
            return None

        try:
            payload = auth.verify_id_token(firebase_token)
        except ValueError:
            msg = _("Invalid firebase ID token.")
            raise exceptions.AuthenticationFailed(msg)
        except (
            auth.ExpiredIdTokenError,
            auth.InvalidIdTokenError,
            auth.RevokedIdTokenError,
        ):
            msg = _("Could not log in.")
            raise exceptions.AuthenticationFailed(msg)

        user = self.authenticate_credentials(payload)

        return user, payload

    def get_token(self, request):
        """
        Returns the firebase ID token from request.
        """
        auth_header = get_authorization_header(request).split()

        if (
            not auth_header
            or auth_header[0].lower() != self.auth_header_prefix.lower().encode()
        ):
            return None

        if len(auth_header) == 1:
            msg = _("Invalid Authorization header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth_header) > 2:
            msg = _(
                "Invalid Authorization header. Token string should not contain spaces."
            )
            raise exceptions.AuthenticationFailed(msg)

        return auth_header[1]

    def authenticate_credentials(self, payload):
        """
        Returns an user that matches the payload's user uid and email.
        """
        if payload["firebase"]["sign_in_provider"] == "anonymous":
            msg = _("Firebase anonymous sign-in is not supported.")
            raise exceptions.AuthenticationFailed(msg)

        if not payload["email_verified"]:
            msg = _("User email not yet confirmed.")
            raise exceptions.AuthenticationFailed(msg)

        uid = payload["uid"]

        try:
            user = self.get_user(uid)
        except User.DoesNotExist:
            firebase_user = auth.get_user(uid)
            user = self.create_user_from_firebase(uid, firebase_user)

        return user

    def get_user(self, uid: str) -> User:
        """Returns the user with given uid"""
        raise NotImplementedError(".get_user() must be overridden.")

    def create_user_from_firebase(
        self, uid: str, firebase_user: auth.UserRecord
    ) -> User:
        """Creates a new user with firebase info"""
        raise NotImplementedError(".create_user_from_firebase() must be overridden.")

    def authenticate_header(self, request):
        return self.auth_header_prefix


class FirebaseAuthentication(BaseFirebaseAuthentication):
    """
    Token based authentication using firebase.
    Clients should authenticate by passing a Firebase ID token in the
    Authorization header using Bearer scheme.
    """

    def get_user(self, uid: str) -> User:
        return User.objects.get(**{self.uid_field: uid})

    def create_user_from_firebase(
        self, uid: str, firebase_user: auth.UserRecord
    ) -> User:
        fields = {
            self.uid_field: uid,
            "email": firebase_user.email,
            "username": generate_username(firebase_user.email),
        }

        return User.objects.create(**fields)
