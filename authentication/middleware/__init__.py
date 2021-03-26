import os

from django.conf import settings

import firebase_admin

cred = firebase_admin.credentials.Certificate(settings.FIREBASE_CONFIG)
default_app = firebase_admin.initialize_app(cred)

from .REST import FirebaseAuthentication
from .channels import FirebaseAuthenticationMiddlewareStack
