from rest_framework import serializers

from core.models import TestCase


class TestCaseSerializer(serializers.ModelSerializer):
    """
    Test Case Serializer
    """

    class Meta:
        model = TestCase
        exclude = []
