# Generated by Django 2.0.6 on 2018-06-26 00:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smida', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='smidamodel',
            old_name='matched_json',
            new_name='data',
        ),
    ]
