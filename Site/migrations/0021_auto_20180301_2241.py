# Generated by Django 2.0.1 on 2018-03-02 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0020_auto_20180301_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='cities',
            name='County',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='cities',
            name='CountyCode',
            field=models.IntegerField(default=-1),
        ),
    ]
