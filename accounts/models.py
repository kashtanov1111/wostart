from random import randint

from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Value, Q 
from django.db.models.functions import Concat
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserQueryset(models.query.QuerySet):

    def active(self):
        return self.filter(active=True)
    
    def with_full_name(self):
        return self.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name'))
    
    def search(self, query):
        return (self.with_full_name()
                    .filter(Q(full_name__icontains=query) |
                            Q(profile__about__icontains=query) |
                            Q(email__icontains=query)
                            ).distinct()
                )

class CustomUserManager(UserManager):

    def get_queryset(self):
        return CustomUserQueryset(self.model, using=self._db)
    
    def with_full_name(self):
        return self.get_queryset().with_full_name()

    def search(self, query):
        return self.get_queryset().search(query)
    
    def all(self):
        return self.get_queryset().ative()

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(
        _("date joined"), default=timezone.now, db_index=True)

    def get_absolute_url(self):
        return reverse('users:user_profile', kwargs={'username': self.username})


    objects = CustomUserManager()

def customuser_post_save_receiver(
    sender, instance, created, *args, **kwargs):
    if created == True:
        UserProfile.objects.create(user=instance)

post_save.connect(customuser_post_save_receiver, sender=CustomUser)

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
    about = models.TextField(max_length=1500, null=True, blank=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    mobile_phone = PhoneNumberField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatars', blank=True, null=True)

    objects = UserProfileManager()
    
    def get_absolute_url(self):
        return reverse('users:user_profile', kwargs={'username': self.user.username})
    
    def __str__(self):
        return self.user.email

