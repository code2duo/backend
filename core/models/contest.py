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
        choices=MatchTypeChoices.choices,
        default=MatchTypeChoices.ONEvONE,
    )  # 1v1 or 2v2
    start_time = models.DateTimeField(auto_now_add=True)

    # this can be max start_time + duration (in minutes) but can be less if teams quit early
    end_time = models.DateTimeField(null=True, blank=True)

    duration = models.PositiveSmallIntegerField(default=30)  # in minutes

    winner = models.SmallIntegerField(null=True, blank=True)
