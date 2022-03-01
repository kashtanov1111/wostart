from random import randint

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Value, Q 
from django.db.models.functions import Concat
from django.template.defaultfilters import slugify

from startups.models import Startup
from tags.models import Tag

class CustomUserQueryset(models.query.QuerySet):

    def with_full_name(self):
        return self.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name'))
    
    def search(self, query):
        return (self.with_full_name()
                    .filter(Q(full_name__icontains=query) |
                            Q(profile__about__icontains=query) |
                            Q(email__icontains=query)
                            )
                )

class CustomUserManager(UserManager):

    def get_queryset(self):
        return CustomUserQueryset(self.model, using=self._db)
    
    def with_full_name(self):
        return self.get_queryset().with_full_name()

    def search(self, query):
        return self.get_queryset().search(query)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


    objects = CustomUserManager()

class UserProfileQueryset(models.query.QuerySet):
    pass

class UserProfileManager(models.Manager):

    def get_queryset(self):
        return UserProfileQueryset(self.model, using=self._db)


class UserProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='profile'
        )
    about = models.TextField(null=True, blank=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    mobile_phone = models.BigIntegerField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatars', blank=True, null=True)
    startups = models.ManyToManyField(Startup, blank=True, null=True)

    objects = UserProfileManager()
    
    def __str__(self):
        return self.user.email
    
    @property
    def startup_list(self):
        return ', '.join([startup.title for startup in self.startups.all()])

