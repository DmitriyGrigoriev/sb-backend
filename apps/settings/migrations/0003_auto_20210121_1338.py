# Generated by Django 3.1 on 2021-01-21 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_auto_20210121_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noseriesline',
            name='last_date_used',
            field=models.DateField(blank=True, null=True, verbose_name='Посл.Исп. Дата'),
        ),
        migrations.AlterField(
            model_name='noseriesline',
            name='last_no_used',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='Посл.Исп. Но'),
        ),
    ]