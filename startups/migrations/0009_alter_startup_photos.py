# Generated by Django 4.0.2 on 2022-03-02 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0008_startup_photos_alter_startup_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='photos',
            field=models.ImageField(blank=True, null=True, upload_to='photos/'),
        ),
    ]
