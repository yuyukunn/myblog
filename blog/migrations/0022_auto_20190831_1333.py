# Generated by Django 2.2.4 on 2019-08-31 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_readnumdate_blog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='readnumdate',
            options={'ordering': ['-readnum_date', '-date_time']},
        ),
    ]
