# Generated by Django 2.2.4 on 2019-08-29 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_remove_readnum_readnum_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='readnum',
            name='readnum_date',
            field=models.IntegerField(default=0),
        ),
    ]
