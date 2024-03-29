import os

from random import randint

from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy

from tags.models import Tag
from config.validators import OptionalSchemeURLValidator

class StartupQueryset(models.QuerySet):

    def search(self, query):
        lookups = (
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(web_site__icontains=query)
        )
        return self.filter(lookups).distinct()

class StartupManager(models.Manager):

    def get_queryset(self):
        return StartupQueryset(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

class Startup(models.Model):
    title = models.CharField(max_length=60,
        help_text='Please enter the title for your startup.')
    slug = models.SlugField(null=True, blank=True, unique=True)
    description = models.TextField(max_length=1500,
        help_text='Please tell us something about your startup.')
    web_site = models.CharField(max_length=200, blank=True, null=True,
        help_text='Please enter the URL of your Startup.',
        verbose_name='Web-site',
        validators=[OptionalSchemeURLValidator()])
    founded = models.DateField(null=True,
        help_text='Please enter the date when your startup was founded.',
        verbose_name='Founding Date', db_index=True)
    founder = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, related_name='startups')

    objects = StartupManager()

    def get_absolute_url(self):
        return reverse('startups:startup_detail', 
                        kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('startups:startup_delete', 
                        kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('startups:startup_update', 
                        kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        slugified_title = slugify(self.title[:40])
        if not self.slug == slugified_title:
            self.slug = slugified_title
            while Startup.objects.filter(slug=self.slug).exists():
                self.slug = self.slug + str(randint(1, 100))
        return super().save(*args, **kwargs)

def image_dir_path(instance, filename):
    startup = instance.startup.slug
    return os.path.join(startup, 'images', filename)

class StartupImage(models.Model):
    startup = models.ForeignKey(
        Startup, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to=image_dir_path, blank=True, null=True, db_index=True)