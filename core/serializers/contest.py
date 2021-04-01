from rest_framework import serializers

from core.models import Contest

from .base import EnumField
from .team import TeamSerializer
from .question import QuestionSerializer


class ContestSerializer(serializers.ModelSerializer):
    """
    Contest Serializer
    """

    teams = TeamSerializer(many=True)
    questions = QuestionSerializer(many=True)

    match_type = EnumField(choices=Contest.MatchTypeChoices)

    class Meta:
        model = Contest
        exclude = []
