from django.db import models

from .question import Question
from .team import Team


class Contest(models.Model):
    """
    Contest DB Model
    """

    class MatchTypeChoices(models.IntegerChoices):
        """
        Match Type Choices
        """

        ONEvONE = 1
        TWOvTWO = 2

    teams = models.ForeignKey(to=Team, on_delete=models.CASCADE, related_name="contest")
    questions = models.ManyToManyField(to=Question, related_name="contests")

    match_type = models.PositiveSmallIntegerField(
        choices=MatchTypeChoices.choices
    )  # 1v1 or 2v2
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()

    winner = models.SmallIntegerField()
