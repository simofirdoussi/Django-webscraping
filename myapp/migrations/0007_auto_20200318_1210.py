# Generated by Django 3.0.3 on 2020-03-18 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20200224_1831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='search',
            name='category',
        ),
        migrations.RemoveField(
            model_name='search',
            name='city',
        ),
    ]