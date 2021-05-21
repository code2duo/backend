from .profile import urlpatterns as profile_urlpatterns
from .matchmaking import urlpatterns as matchmaking_urlpatterns
from .questions import urlpatterns as question_urlpatterns

urlpatterns = profile_urlpatterns + matchmaking_urlpatterns + question_urlpatterns
