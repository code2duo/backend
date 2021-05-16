from django.contrib import admin

from core.models import TestCase


class TestCaseAdmin(admin.TabularInline):
    model = TestCase
