from enum import Enum

from rest_framework import serializers


class EnumField(serializers.Field):
    """
    Enum Field Serializer
    """

    choices = None

    def __init__(self, choices, allow_blank=False, *args, **kwargs):
        super().__init__(args, kwargs)
        self.choices = choices
        self.allow_blank = allow_blank

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        try:
            return self.choices[data]
        except KeyError:
            self.fail('invalid_choice', input=data)

    def to_representation(self, value):
        if value in ('', None):
            return value
        return self.choices(value).name
