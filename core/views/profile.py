from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from core.models import Profile
from core.serializers import UserSerializer, ProfileSerializer

User = get_user_model()


class GetUsername(APIView):
    def get(self, request, *args, **kwargs):
        user: User = request.user
        username = None

        try:
            _ = user.profile
            username = user.username
        except Profile.DoesNotExist:
            pass

        data = {"status": "OK", "message": {"username": username}}

        return Response(
            data=data,
            status=status.HTTP_200_OK,
        )


class GetProfile(RetrieveAPIView):
    """
    Get or Create Profile
    """

    lookup_field = "username"
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CreateProfile(CreateAPIView):
    """
    Create Profile API
    """

    serializer_class = ProfileSerializer

    @swagger_auto_schema(request_body=ProfileSerializer)
    def create(self, request, *args, **kwargs):
        user: User = request.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()
        request.data["user"] = request.user.pk
        return super().create(request, *args, **kwargs)
