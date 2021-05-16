from django.db import models

from .contest import Contest
from .enums import LevelChoices


class Question(models.Model):
    """
    Question DB Model
    """

    contests = models.ManyToManyField(to=Contest, related_name="questions", blank=True)

    question = models.TextField()
    example = models.TextField()

    level = models.PositiveSmallIntegerField(choices=LevelChoices.choices)
