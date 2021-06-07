from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView, status
from rest_framework.response import Response

from core.models import Searching, Contest, MatchRoom

User = get_user_model()


class CreateMatchLinkView(APIView):
    """
    Create Match Link API
    """

    @swagger_auto_schema()
    def post(self, *args, **kwargs):

        match_room_obj = MatchRoom()
        match_room_obj.save()

        return Response(
            data={"status": "OK", "message": {"link": match_room_obj.room_id}},
            status=status.HTTP_201_CREATED,
        )


class JoinMatchView(APIView):
    """
    Join Match with Link
    """

    @swagger_auto_schema()
    def post(self, request, room_id: str, *args, **kwargs):
        try:
            searching_obj = Searching.objects.get(room_name__exact=room_id)
        except Searching.DoesNotExist:
            return Response(data={"status": "FAIL", "message": "Room Does not Exists"})

        # participant 1 -- who created the link
        # participant 2 -- who joined the link
        contest_obj = Contest(
            room_id=searching_obj.room_name,
            participant_1=searching_obj.user.profile,
            participant_2=request.user.profile
        )
        # TODO add questions
        contest_obj.save()

        searching_obj.delete()

        return Response(
            data={
                "status": "OK",
                "message": {

                }
            }
        )
