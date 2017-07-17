from django.db import models
from django.utils import timezone


class Api(models.Model):
    owner = models.ForeignKey("auth.User")
    name = models.TextField()
    version = models.TextField()
    created = models.DateTimeField(
        default=timezone.now)
    modified = models.DateTimeField(
        default=timezone.now)
    swagger = models.TextField()

    def __str__(self):
return self.name
