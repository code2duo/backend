from django.urls import path

from core.views import GetProfile, CreateProfile

urlpatterns = [
    path(
        "profile/<str:username>",
        GetProfile.as_view(),
        name="get_create_user_profile",
    ),
    path("profile", CreateProfile.as_view(), name="create_profile"),
]
