# Generated by Django 2.2.4 on 2019-08-14 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lets_party', '0002_auto_20190814_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='letspartymodel',
            name='period',
            field=models.CharField(default='', max_length=30, verbose_name='Період звіту'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='letspartymodel',
            name='type',
            field=models.CharField(choices=[('nacp', 'Звіти партій (НАЗК)'), ('parliament', 'Попередні звіти парламентських виборів (ЦВК)'), ('president', 'Попередні звіти президентських виборів (ЦВК)'), ('parliament_final', 'Звіти парламентських виборів (ЦВК)'), ('president_final', 'Звіти президентських виборів (ЦВК)')], max_length=20, verbose_name='Джерело даних'),
        ),
    ]
