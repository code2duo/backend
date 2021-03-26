from django.conf import settings
from django.db import models


class Participant(models.Model):
    """
    Participant DB Model
    """

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, related_name="+", on_delete=models.CASCADE
    )

    score = models.PositiveSmallIntegerField(default=0)


class Team(models.Model):
    """
    Team DB Model
    """

    members = models.ForeignKey(
        to=Participant, related_name="team", on_delete=models.CASCADE
    )

    score = models.PositiveSmallIntegerField(default=0)
