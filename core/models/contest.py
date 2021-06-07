from django.db import models

from code2duo import settings

from .profile import Profile
from .question import Question
from .enums import MatchTypeChoices


class Contest(models.Model):
    """
    Contest DB Model
    """

    room_id = models.CharField(max_length=12, null=True, blank=True, unique=True)

    questions = models.ManyToManyField(Question, related_name="contest", blank=True)

    # team 1
    participant_1 = models.ForeignKey(
        Profile,
        related_name="contest_1",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    score_1 = models.PositiveSmallIntegerField(default=0)

    # team 2
    participant_2 = models.ForeignKey(
        Profile,
        related_name="contest_2",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    score_2 = models.PositiveSmallIntegerField(default=0)

    match_type = models.PositiveSmallIntegerField(
        choices=MatchTypeChoices.choices,
        default=MatchTypeChoices.ONEvONE,
    )  # 1v1 or 2v2
    start_time = models.DateTimeField(auto_now_add=True)

    # this can be max start_time + duration (in minutes) but can be less if teams quit early
    end_time = models.DateTimeField(null=True, blank=True)

    duration = models.PositiveSmallIntegerField(default=60)  # in minutes

    winner = models.SmallIntegerField(null=True, blank=True)

    is_ongoing = models.BooleanField(default=True)


class Searching(models.Model):
    """
    Searching DB Model
    """

    room_name = models.CharField(max_length=12, unique=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="+"
    )
    type = models.PositiveSmallIntegerField(
        choices=MatchTypeChoices.choices, default=MatchTypeChoices.ONEvONE
    )


class MatchRoom(models.Model):
    """
    Room DB Model
    """

    room_id = models.CharField(max_length=12, unique=True)
    participant_1 = models.ForeignKey(
        to=Profile, on_delete=models.DO_NOTHING, related_name="+", blank=True, null=True,
    )
    participant_2 = models.ForeignKey(
        to=Profile, on_delete=models.DO_NOTHING, related_name="+", blank=True, null=True,
    )

    def __str__(self):
        return f"<MatchRoom(room_id={self.room_id})>"
