# Generated by Django 2.0.1 on 2018-02-25 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0018_auto_20180225_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='Geography',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Country', models.CharField(default='', max_length=64)),
                ('CountryCode', models.IntegerField(default=-1)),
                ('Area', models.CharField(default='', max_length=64)),
                ('AreaCode', models.IntegerField(default=-1)),
                ('SubArea', models.CharField(default='', max_length=64)),
                ('SubAreaCode', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='JobSkillRegionDateCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('posted_count', models.IntegerField(default=0)),
                ('geography', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Site.Geography')),
                ('job_skill', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Site.JobSkill')),
            ],
        ),
    ]
