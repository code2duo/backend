from rest_framework import serializers

from core.models import Team, Participant

# from .user import UserSerializer


# class ParticipantSerializer(serializers.ModelSerializer):
#     """
#     Participant Serializer
#     """
#
#     user = UserSerializer()
#
#     class Meta:
#         model = Participant


class TeamSerializer(serializers.ModelSerializer):
    """
    Team Serializer
    """

    # members = ParticipantSerializer(many=True)

    class Meta:
        model = Team
        exclude = []
