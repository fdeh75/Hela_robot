# Generated by Django 3.1.5 on 2021-02-06 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='employment_des',
            field=models.TextField(blank=True),
        ),
    ]
