# Generated by Django 2.0.1 on 2018-03-02 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0021_auto_20180301_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobSkillCityDateCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('posted_count', models.IntegerField(default=0)),
                ('city', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Site.Cities')),
                ('job', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Site.Jobs')),
                ('skill', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Site.Skills')),
            ],
        ),
    ]