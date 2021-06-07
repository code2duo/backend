from django.conf import settings
from django.db import models

from .enums import SexChoices, ProgrammingLanguageChoices, LevelChoices


class Profile(models.Model):
    """
    Profile Model
    """

    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="profile"
    )

    sex = models.PositiveSmallIntegerField(
        choices=SexChoices.choices, blank=True, null=True
    )
    profile_img = models.URLField(blank=True, null=True)
    state = models.PositiveSmallIntegerField(blank=True, null=True)
    programming_lang = models.PositiveSmallIntegerField(
        choices=ProgrammingLanguageChoices.choices,
        default=ProgrammingLanguageChoices.CPP,
    )
    rank = models.PositiveIntegerField(blank=True, null=True)
    no_of_questions_solved = models.IntegerField(default=0)
    no_of_contests = models.IntegerField(default=0)

    level = models.PositiveSmallIntegerField(
        choices=LevelChoices.choices, blank=True, null=True, default=LevelChoices.NOOB,
    )

    is_searching = models.BooleanField(default=False)
