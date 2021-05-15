from django.conf import settings

import firebase_admin

if settings.DEBUG:
    cred = firebase_admin.credentials.Certificate(settings.FIREBASE_CONFIG)
    default_app = firebase_admin.initialize_app(cred)
else:
    # initializing to default gcp service account on Cloud Run
    default_app = firebase_admin.initialize_app()

from .REST import FirebaseAuthentication
from .channels import FirebaseAuthenticationMiddlewareStack
