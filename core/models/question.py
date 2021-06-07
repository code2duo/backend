from django.db import models

from .enums import LevelChoices


class Question(models.Model):
    """
    Question DB Model
    """

    question = models.TextField()
    example = models.TextField()

    level = models.PositiveSmallIntegerField(choices=LevelChoices.choices)
