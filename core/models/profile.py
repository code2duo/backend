from django.conf import settings
from django.db import models

from .contest import Contest


class Profile(models.Model):
    """
    Profile Model
    """

    class SexChoices(models.IntegerChoices):
        """
        Sex choices
        """

        MALE = 1
        FEMALE = 2
        OTHERS = 3

    class ProgrammingLanguageChoices(models.IntegerChoices):
        """
        Programming Languages Choices
        """

        C = 1
        CPP = 2
        JAVA = 3
        PYTHON = 4

    class LevelChoices(models.IntegerChoices):
        """
        Level Choices
        """

        NOOB = 1
        INTERMEDIATE = 2
        PRO = 3

    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="profile"
    )
    contests = models.ForeignKey(
        to=Contest, on_delete=models.CASCADE, null=True, blank=True
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
        choices=LevelChoices.choices, blank=True, null=True
    )

    is_searching = models.BooleanField(default=False)
