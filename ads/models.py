from random import randint

from django.db import models
from django.template.defaultfilters import slugify

from tags.models import Tag
from startups.models import Startup


class Ad(models.Model):
    POSITIONS = (
        ('F', 'Co-Founder'),
        ('E', 'Employee'),
    )
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True)
    position = models.CharField(max_length=1, choices=POSITIONS)
    description = models.TextField()
    share = models.DecimalField(max_digits=4, decimal_places=2)
    startup = models.ForeignKey(
        Startup, on_delete=models.CASCADE, related_name='ads')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while Ad.objects.filter(slug=self.slug).exists():
                self.slug = self.slug + str(randint(1, 100))
        return super().save(*args, **kwargs)