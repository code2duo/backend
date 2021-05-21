from django.urls import path

from core.views import CreateMatchLinkView, JoinMatchView

urlpatterns = [
    path(
        "create/room-link",
        CreateMatchLinkView.as_view(),
        name="create_room_link",
    ),
    path("join/<str:room_id>", JoinMatchView.as_view(), name="join_match_view"),
]
