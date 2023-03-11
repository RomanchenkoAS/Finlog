# Generated by Django 4.1.7 on 2023-03-11 10:02

from django.db import migrations, models
import django.db.models.deletion
import log.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('log', '0002_remove_entry_category_entry_content_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='content_type',
            field=models.ForeignKey(default=log.models.get_default_category_ct, on_delete=django.db.models.deletion.SET_DEFAULT, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='object_id',
            field=models.PositiveIntegerField(default=log.models.get_default_category),
        ),
    ]
