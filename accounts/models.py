from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='profile'
        )
    age = models.PositiveIntegerField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatars', blank=True, null=True)

