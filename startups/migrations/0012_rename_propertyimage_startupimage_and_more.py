# Generated by Django 4.0.2 on 2022-03-02 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0011_startup_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PropertyImage',
            new_name='StartupImage',
        ),
        migrations.RenameField(
            model_name='startupimage',
            old_name='property',
            new_name='startup',
        ),
    ]
