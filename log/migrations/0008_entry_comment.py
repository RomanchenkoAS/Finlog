# Generated by Django 4.1.6 on 2023-02-15 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0007_alter_entry_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='comment',
            field=models.CharField(blank=True, max_length=3),
        ),
    ]
