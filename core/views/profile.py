from django.contrib.auth import get_user_model
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

    def create(self, request, *args, **kwargs):
        user: User = request.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()
        request.data["user"] = request.user.pk
        return super().create(request, args, kwargs)