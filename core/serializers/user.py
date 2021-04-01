from django.contrib.auth import get_user_model
from rest_framework import serializers

from .profile import ProfileSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """

    profile = ProfileSerializer()

    class Meta:
        model = User
        exclude = [
            "id",
            "uid",
            "password",
            "is_superuser",
            "is_active",
            "last_login",
        ]
