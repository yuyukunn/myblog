# Generated by Django 2.2.4 on 2019-08-31 02:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_remove_readnumdate_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='readnumdate',
            name='blog',
            field=models.OneToOneField(default=django.utils.timezone.now, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Blog'),
            preserve_default=False,
        ),
    ]
