from .profile import urlpatterns as profile_urlpatterns
from .questions import urlpatterns as question_urlpatterns

urlpatterns = profile_urlpatterns + question_urlpatterns
