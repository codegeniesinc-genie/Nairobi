# Generated by Django 5.0 on 2024-02-24 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_author',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_organizer',
            field=models.BooleanField(default=False),
        ),
    ]