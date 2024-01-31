from django.views.generic.base import TemplateView
from django.shortcuts import render, get_object_or_404
from .models import Event,Blog


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
        events = Event.objects.filter(is_published=True)
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

        context['latest_blogs'] = all_blogs.filter(category='latest')
        context['upcoming_events'] = all_blogs.filter(category='upcoming')
        context['tech_entertainment'] = all_blogs.filter(category='tech')
        context['past_event_reviews'] = all_blogs.filter(category='reviews')
        context['artists_corner'] = all_blogs.filter(category='artists')

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
