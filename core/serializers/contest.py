from rest_framework import serializers

from core.models import Contest
from core.models.enums import MatchTypeChoices

from .base import EnumField
from .question import QuestionSerializer


class ContestSerializer(serializers.ModelSerializer):
    """
    Contest Serializer
    """

    questions = QuestionSerializer(many=True)

    match_type = EnumField(choices=MatchTypeChoices.choices)

    class Meta:
        model = Contest
        exclude = []
