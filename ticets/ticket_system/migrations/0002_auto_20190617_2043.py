# Generated by Django 2.2.2 on 2019-06-17 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date_and_time',
            field=models.DateTimeField(verbose_name='End date and time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date_and_time',
            field=models.DateTimeField(verbose_name='Start date and time'),
        ),
    ]