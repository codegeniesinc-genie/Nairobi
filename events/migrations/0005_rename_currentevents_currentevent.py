# Generated by Django 5.0 on 2023-12-12 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_rename_events_event'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CurrentEvents',
            new_name='CurrentEvent',
        ),
    ]