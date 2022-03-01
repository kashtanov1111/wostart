from random import randint

from django.db import models
from django.template.defaultfilters import slugify

from tags.models import Tag

class Startup(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField()
    web_site = models.URLField(blank=True, null=True)
    founded = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while Startup.objects.filter(slug=self.slug).exists():
                self.slug = self.slug + str(randint(1, 100))
        return super().save(*args, **kwargs)