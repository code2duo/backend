from rest_framework import serializers


class EnumField(serializers.Field):
    """
    Enum Field Serializer
    """

    choices = None

    def __init__(self, choices, *args, **kwargs):
        self.choices = choices
        super(EnumField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if data is None:
            return None

        try:
            return self.choices[data]
        except KeyError:
            self.fail("invalid_choice", input=data)

    def to_representation(self, value):
        if value is None:
            return None

        return self.choices(value).name
