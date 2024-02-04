# fix_author_id.py

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nbo.settings')
django.setup()

from events.models import Blog
from events.models import CustomUser

def correct_author_id():
    try:
        # Get the CustomUser instance for the user with the username 'Siama'
        user = CustomUser.objects.get(username='Siama')
    except CustomUser.DoesNotExist:
        print("User 'Siama' does not exist")
        return

    # Find all blog posts with author_id as the ID of the user 'Siama'
    invalid_posts = Blog.objects.filter(author__username='Siama')

    # Update the author_id for each of these blog posts
    for post in invalid_posts:
        post.author_id = user.id
        post.save()

    print("Author ID corrected successfully")

if __name__ == "__main__":
    correct_author_id()
