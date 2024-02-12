from tinymce.models import HTMLField
from django.db import models


class Event(models.Model):

    CATEGORY_CHOICES = [
    ('upcoming', 'Upcoming Events'),
    ('past', 'Past Event'),
    ]

    title = models.CharField(max_length=100)
    county = models.CharField(max_length=50)
    category_type = models.CharField(max_length=50,  choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    contact_email = models.EmailField()
    is_published = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title
    
class Blog(models.Model):

    CATEGORY_CHOICES = [
    ('latest', 'Latest'),
    ('reviews', 'Past Event Reviews'),
    ('upcoming', 'Upcoming Events Reviews'),
    ('tech', 'Tech in the Entertainment Industry'),
    ('artists', "Artist's Corner"),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    short_description =HTMLField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES)
    content = HTMLField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_related_posts(self):
        return Blog.objects.filter(category=self.category).exclude(id=self.id)


