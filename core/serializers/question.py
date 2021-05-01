from rest_framework import serializers

from core.models import Question
from core.models.enums import LevelChoices

from .base import EnumField
from .testcase import TestCaseSerializer


class QuestionSerializer(serializers.ModelSerializer):
    """
    Question Serializer
    """

    test_cases = TestCaseSerializer(many=True)

    level = EnumField(choices=LevelChoices.choices, required=True)

    class Meta:
        model = Question
        exclude = []
