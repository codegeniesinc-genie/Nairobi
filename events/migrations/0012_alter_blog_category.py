# Generated by Django 5.0 on 2024-01-22 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_remove_blog_category_type_blog_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='category',
            field=models.CharField(choices=[('latest', 'Latest'), ('event_reviews', 'Event Reviews'), ('upcoming_events', 'Upcoming Events Reviews'), ('tech_entertainment', 'Tech in the Entertainment Industry'), ('artists_corner', "Artist's Corner")], default=[('latest', 'Latest'), ('event_reviews', 'Event Reviews'), ('upcoming_events', 'Upcoming Events Reviews'), ('tech_entertainment', 'Tech in the Entertainment Industry'), ('artists_corner', "Artist's Corner")], max_length=50),
        ),
    ]