from rest_framework import serializers

from core.models import Question

from .testcase import TestCaseSerializer


class QuestionSerializer(serializers.ModelSerializer):
    """
    Question Serializer
    """

    test_cases = TestCaseSerializer(many=True)

    class Meta:
        model = Question
        exclude = []
