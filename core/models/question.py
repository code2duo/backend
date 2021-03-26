from django.db import models

from .testcase import TestCase


class Question(models.Model):
    """
    Question DB Model
    """

    test_cases = models.ForeignKey(
        to=TestCase, related_name="question", on_delete=models.CASCADE
    )

    question = models.TextField()
    example = models.TextField()
