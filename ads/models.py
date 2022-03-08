from random import randint

from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse

from tags.models import Tag
from startups.models import Startup


class AdQueryset(models.QuerySet):

    def search(self, query):
        lookups = (
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(share__icontains=query) |
            Q(startup__title__icontains=query)
        )
        return self.filter(lookups).distinct()

class AdManager(models.Manager):

    def get_queryset(self):
        return AdQueryset(self.model, using=self._db)
    
    def search(self, query):
        return self.get_queryset().search(query)

class Ad(models.Model):
    POSITIONS = (
        ('F', 'Co-Founder'),
        ('E', 'Employee'),
    )
    title = models.CharField(max_length=60,
        help_text='Please enter the title for your ad.')
    slug = models.SlugField(null=True, blank=True, unique=True)
    position = models.CharField(max_length=1, choices=POSITIONS,
        help_text='Please specify the position.')
    description = models.TextField(max_length=1500,
        help_text='Please tell us more about it.',
        verbose_name='About')
    share = models.DecimalField(max_digits=4, decimal_places=2,
        help_text='Please specify the share.')
    startup = models.ForeignKey(
        Startup, on_delete=models.CASCADE, related_name='ads',
        blank=True, null=True,
        help_text='Please choose the startup.')
    user = models.ForeignKey(get_user_model(),
        on_delete=models.CASCADE, related_name='ads')
    created = models.DateTimeField(auto_now_add=True)

    objects = AdManager()

    def __str__(self):
        return self.title

    def position_verbose(self):
        return dict(self.POSITIONS)[self.position]

    def get_absolute_url(self):
        return reverse("ads:ad_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        slugified_title = slugify(self.title[:40])
        if not self.slug == slugified_title:
            self.slug = slugified_title
            while Ad.objects.filter(slug=self.slug).exists():
                self.slug = self.slug + str(randint(1, 100))
        return super().save(*args, **kwargs)