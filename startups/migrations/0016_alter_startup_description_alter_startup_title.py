# Generated by Django 4.0.2 on 2022-03-03 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0015_alter_startup_founder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='description',
            field=models.TextField(max_length=1500),
        ),
        migrations.AlterField(
            model_name='startup',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
