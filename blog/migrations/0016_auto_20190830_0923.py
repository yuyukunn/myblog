# Generated by Django 2.2.4 on 2019-08-30 01:23

from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20190829_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readnumdate',
            name='date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
