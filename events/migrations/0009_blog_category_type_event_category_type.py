# Generated by Django 5.0 on 2024-01-08 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_remove_event_about_blog_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='category_type',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='category_type',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
    ]