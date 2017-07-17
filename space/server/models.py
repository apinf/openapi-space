from django.db import models
from django.utils import timezone


class Api(models.Model):
    owner = models.ForeignKey("auth.User")
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    created = models.DateTimeField(
        default=timezone.now)
    modified = models.DateTimeField(
        default=timezone.now)
    swagger = models.TextField()
