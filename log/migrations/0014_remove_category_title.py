# Generated by Django 4.1.7 on 2023-03-07 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0013_category_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='title',
        ),
    ]
