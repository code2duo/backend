from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Authentication User class
    """

    UID_FIELD = "uid"

    uid_validator = UnicodeUsernameValidator()

    uid = models.CharField(
        _("uid"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[uid_validator],
        error_messages={
            "unique": _("A user with that uid already exists."),
        },
    )
