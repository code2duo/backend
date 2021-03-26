from django.db import models


class TestCase(models.Model):
    """
    Test Case DB Model
    """

    public = models.BooleanField(default=True)

    input = models.TextField()
    output = models.TextField()
