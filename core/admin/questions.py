from django.contrib import admin

from core.models import Question

from .testcases import TestCaseAdmin


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        TestCaseAdmin,
    ]


admin.site.register(Question, QuestionAdmin)
