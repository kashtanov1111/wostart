# Generated by Django 4.0.2 on 2022-03-02 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0013_alter_startupimage_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='startup',
            old_name='user',
            new_name='founder',
        ),
    ]
