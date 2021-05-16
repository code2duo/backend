from django.db import models

from .question import Question


class TestCase(models.Model):
    """
    Test Case DB Model
    """

    question = models.ForeignKey(
        to=Question, related_name="test_cases", on_delete=models.CASCADE
    )

    public = models.BooleanField(default=True)

    input = models.TextField()
    output = models.TextField()
