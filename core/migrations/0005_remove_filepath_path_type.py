# Generated by Django 3.1.5 on 2021-01-19 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210108_1954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filepath',
            name='path_type',
        ),
    ]
