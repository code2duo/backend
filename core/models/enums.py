from django.db import models


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


class MatchTypeChoices(models.IntegerChoices):
    """
    Match Type Choices
    """

    ONEvONE = 1
    TWOvTWO = 2
