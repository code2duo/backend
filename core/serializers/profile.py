from rest_framework import serializers

from core.models import Profile
from core.models.enums import ProgrammingLanguageChoices

from .base import EnumField
from .contest import ContestSerializer


class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile Serializer
    """

    contests = ContestSerializer(many=True, read_only=True)

    programming_lang = EnumField(choices=ProgrammingLanguageChoices, required=False)

    class Meta:
        model = Profile
        exclude = [
            "id",
        ]
        extra_kwargs = {
            "user": {"write_only": True},
        }
