# Generated by Django 2.0.6 on 2018-07-12 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vkks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vkksmodel',
            name='source',
        ),
    ]