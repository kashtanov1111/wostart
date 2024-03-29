# Generated by Django 4.0.2 on 2022-03-05 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0018_alter_startup_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='description',
            field=models.TextField(help_text='Please tell us something about your startup.', max_length=1500),
        ),
        migrations.AlterField(
            model_name='startup',
            name='founded',
            field=models.DateField(help_text='Please enter the date when your startup was founded.', null=True, verbose_name='Founding Date'),
        ),
        migrations.AlterField(
            model_name='startup',
            name='title',
            field=models.CharField(help_text='Please enter the title for your startup.', max_length=60),
        ),
        migrations.AlterField(
            model_name='startup',
            name='web_site',
            field=models.URLField(blank=True, null=True, verbose_name='Web-Site'),
        ),
    ]
