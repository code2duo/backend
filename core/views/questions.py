from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView

from core.serializers import QuestionSerializer


class CreateQuestionView(CreateAPIView):
    """
    Create Profile API
    """

    serializer_class = QuestionSerializer

    @swagger_auto_schema(request_body=QuestionSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
