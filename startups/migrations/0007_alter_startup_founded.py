# Generated by Django 4.0.2 on 2022-03-01 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0006_startup_founded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='founded',
            field=models.DateField(null=True),
        ),
    ]
