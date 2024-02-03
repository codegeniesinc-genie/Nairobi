from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(validators=[MaxLengthValidator(350)])
    county = models.CharField(max_length=50)
    category_type = models.CharField(max_length=75,  null=True, blank=True)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.CharField(max_length=100)
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
    short_description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES)
    content = models.TextField()
    author = models.CharField(max_length=1000,blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_related_posts(self):
        return Blog.objects.filter(category=self.category).exclude(id=self.id)


# Represents a dashboard for tracking event statistics    
class Dashboard(models.Model):
    organizer = models.ForeignKey('Organizer', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    total_tickets = models.IntegerField(default=0)
    tickets_sold = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.organizer} - {self.event} Dashboard"



# Represents an event organizer with contact details
class Organizer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True) 

    def __str__(self):
        return f"{self.name} ({self.email})"


# Represents current events happening within the next 24 hours
class CurrentEvent(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    organizer = models.CharField(max_length=100)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        """Check if the event is upcoming within the next 24 hours."""
        now = timezone.now()
        return now < self.event_datetime < now + timezone.timedelta(hours=24)



