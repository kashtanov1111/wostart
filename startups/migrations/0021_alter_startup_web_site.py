# Generated by Django 4.0.2 on 2022-03-06 13:06

import config.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0020_alter_startup_web_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='web_site',
            field=models.URLField(blank=True, help_text='Please enter the URL of your Startup.', null=True, validators=[config.validators.OptionalSchemeURLValidator], verbose_name='Web-site'),
        ),
    ]
