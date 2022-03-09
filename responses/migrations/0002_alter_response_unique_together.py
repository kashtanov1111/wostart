# Generated by Django 4.0.2 on 2022-03-09 09:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ads', '0006_alter_ad_position'),
        ('responses', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='response',
            unique_together={('user', 'ad')},
        ),
    ]
