# Generated by Django 4.0.2 on 2022-02-27 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_userprofile_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='tags',
        ),
    ]