# Generated by Django 2.2.4 on 2019-08-30 01:38

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20190830_0930'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='readnumdate',
            options={'ordering': ['-date_time']},
        ),
        migrations.AlterField(
            model_name='readnumdate',
            name='date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]