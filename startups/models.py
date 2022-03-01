from random import randint

from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify

from tags.models import Tag

class StartupQueryset(models.QuerySet):

    def search(self, query):
        lookups = (
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(web_site__icontains=query)
        )
        return self.filter(lookups)

class StartupManager(models.Manager):

    def get_queryset(self):
        return StartupQueryset(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

class Startup(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField()
    web_site = models.URLField(blank=True, null=True)
    founded = models.DateField(null=True)

    objects = StartupManager()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while Startup.objects.filter(slug=self.slug).exists():
                self.slug = self.slug + str(randint(1, 100))
        return super().save(*args, **kwargs)