from django.urls import path

from core.views import CreateQuestionView

urlpatterns = [
    path(
        "question/create",
        CreateQuestionView.as_view(),
        name="add_question",
    ),
]
