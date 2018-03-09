from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User)
    profession = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    employment = models.CharField(max_length=255)
    avatar = models.FileField(blank=True, null=True, default=None)

    def __str__(self):
        return self.user.username

