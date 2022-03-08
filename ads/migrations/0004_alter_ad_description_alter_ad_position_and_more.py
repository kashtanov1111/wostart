# Generated by Django 4.0.2 on 2022-03-08 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0025_alter_startup_web_site'),
        ('ads', '0003_ad_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='description',
            field=models.TextField(help_text='Please tell us more about it.', max_length=1500, verbose_name='About'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='position',
            field=models.CharField(choices=[('F', 'Co-Founder'), ('E', 'Employee')], help_text='Please specify the position.', max_length=1),
        ),
        migrations.AlterField(
            model_name='ad',
            name='share',
            field=models.DecimalField(decimal_places=2, help_text='Please specify the share.', max_digits=4),
        ),
        migrations.AlterField(
            model_name='ad',
            name='startup',
            field=models.ForeignKey(blank=True, help_text='Please choose the startup.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ads', to='startups.startup'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='title',
            field=models.CharField(help_text='Please enter the title for your ad.', max_length=60),
        ),
    ]