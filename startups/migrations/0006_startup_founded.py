# Generated by Django 4.0.2 on 2022-03-01 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0005_startup_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='startup',
            name='founded',
            field=models.DateField(blank=True, null=True),
        ),
    ]