from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from core.serializers import UserSerializer, ProfileSerializer

User = get_user_model()


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
        print(request.data)
        return super().create(request, *args, **kwargs)
