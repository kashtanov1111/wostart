# Generated by Django 4.0.3 on 2022-03-18 09:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_userprofile_mobile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='date joined'),
        ),
    ]
