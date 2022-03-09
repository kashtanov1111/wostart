from django.contrib.auth import get_user_model
from django.db import models

from ads.models import Ad

class Response(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='responses')
    ad = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name='reponses')

    class Meta:
        unique_together = ['user', 'ad']
    
    def __str__(self):
        return '%s to %s' % (self.user.username, self.ad.slug)

    