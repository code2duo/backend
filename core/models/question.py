from django.db import models

from .testcase import TestCase
from .enums import LevelChoices


class Question(models.Model):
    """
    Question DB Model
    """

    test_cases = models.ForeignKey(
        to=TestCase, related_name="question", on_delete=models.CASCADE
    )

    question = models.TextField()
    example = models.TextField()

    level = models.PositiveSmallIntegerField(choices=LevelChoices.choices)
