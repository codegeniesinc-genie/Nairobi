from django.views.generic.base import TemplateView, View
from django.shortcuts import render, get_object_or_404
from .models import Event,Blog
from django.http import JsonResponse

class LoadMorePostsView(View):
    def get(self, request):
        category = request.GET.get('category')
        page = int(request.GET.get('page', 1))
        per_page = 5
        start_index = (page - 1) * per_page
        end_index = start_index + per_page

        # Assuming BlogPost model has fields like image, title, category, short_description, etc.
        posts = Blog.objects.filter(category=category)[start_index:end_index]

        data = []
        for post in posts:
            data.append({
                'image': post.image.url,
                'title': post.title,
                'url': post.get_absolute_url(),  # Assuming you have a method to get the post URL
                'category': post.category,
                'short_description': post.short_description
            })

        return JsonResponse(data, safe=False)

class HomePageView(TemplateView):
    template_name = 'events/homepage.html'
    def get_context_data(self, **kwargs):
        events = Event.objects.filter(is_published=True)
        context = {'events': events}
        return context

class DashBoardView(TemplateView):
    template_name = 'events/dashboard.html'

class EventsPageView(TemplateView):
    template_name = 'events/events.html'
    def get_context_data(self, **kwargs):
        events = Event.objects.filter(is_published=True).order_by('-pub_date')
        context = {'events': events}
        return context

class AboutPageView(TemplateView):
    template_name = 'events/about.html'

class ContactPageView(TemplateView):
    template_name = 'events/contact.html'

class PrivacyPolicyPageView(TemplateView):
    template_name = 'events/policy.html'

class BlogPageView(TemplateView):
    template_name = 'events/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_blogs = Blog.objects.all()

        context['latest_blogs'] = all_blogs.filter(category='latest').order_by('-pub_date')
        context['upcoming_events'] = all_blogs.filter(category='upcoming').order_by('-pub_date')
        context['tech_entertainment'] = all_blogs.filter(category='tech').order_by('-pub_date')
        context['past_event_reviews'] = all_blogs.filter(category='reviews').order_by('-pub_date')
        context['artists_corner'] = all_blogs.filter(category='artists').order_by('-pub_date')

        return context    


def single_post(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    category = blog.category

    next_post = Blog.objects.filter(category=category, pub_date__gt=blog.pub_date).order_by('pub_date').first()
    prev_post = Blog.objects.filter(category=category, pub_date__lt=blog.pub_date).order_by('-pub_date').first()

    latest_blogs = Blog.objects.exclude(id=blog.id).order_by('-pub_date')[:5]  

    context = {
        'blog': blog,
        'next_post': next_post,
        'prev_post': prev_post,
        'latest_blogs': latest_blogs,
    }
    return render(request, 'events/singlePost.html', context)

class CheckOutPageView(TemplateView):
    template_name = 'events/checkout.html'

class PaymentPageView(TemplateView):
    template_name = 'events/payment.html'
