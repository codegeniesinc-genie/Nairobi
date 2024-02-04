from django.http import HttpResponseForbidden
from django.views.generic.base import TemplateView, View
from django.shortcuts import render, get_object_or_404
from .models import Event,Blog
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from .models import CustomUser, Event, Blog




class HomePageView(TemplateView):
    template_name = 'events/homepage.html'
    def get_context_data(self, **kwargs):
        events = Event.objects.filter(is_published=True)
        context = {'events': events}
        return context


def blog_posts_by_author(request, author_name):
    blog_posts = Blog.objects.filter(author__username=author_name)
    return render(request, 'blog_posts_by_author.html', {'blog_posts': blog_posts, 'author_name': author_name})


class DashBoardView(TemplateView):
    template_name = 'events/dashboard.html'

# Decorator to restrict access to admin only
def admin_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != CustomUser.ADMIN:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return wrapped_view

# Decorator to restrict access to event organizers only
def event_organizer_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != CustomUser.EVENT_ORGANIZER:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return wrapped_view

# Decorator to restrict access to blog authors only
def blog_author_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != CustomUser.BLOG_AUTHOR:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return wrapped_view

# Login view
class CustomLoginView(LoginView):
    template_name = 'login.html'

# Logout view
class CustomLogoutView(LogoutView):
    pass

# Registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            role = form.cleaned_data.get('role')
            user = authenticate(username=username, password=form.cleaned_data.get('password1'))
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

@login_required
def edit_event(request, pk):
    event = Event.objects.get(pk=pk)
    if request.user != event.organizer:
        return redirect('home')
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'edit_event.html', {'form': form})

@login_required
def delete_event(request, pk):
    event = Event.objects.get(pk=pk)
    if request.user != event.organizer:
        return redirect('home')
    if request.method == 'POST':
        event.delete()
        return redirect('home')
    return render(request, 'delete_event.html', {'event': event})

@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('blog_post_detail', pk=blog_post.pk)
    else:
        form = BlogForm()
    return render(request, 'create_blog_post.html', {'form': form})

@login_required
def edit_blog_post(request, pk):
    blog_post = Blog.objects.get(pk=pk)
    if request.user != blog_post.author:
        return redirect('home')
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('blog_post_detail', pk=blog_post.pk)
    else:
        form = BlogForm(instance=blog_post)
    return render(request, 'edit_blog_post.html', {'form': form})

@login_required
def delete_blog_post(request, pk):
    blog_post = Blog.objects.get(pk=pk)
    if request.user != blog_post.author:
        return redirect('home')
    if request.method == 'POST':
        blog_post.delete()
        return redirect('home')
    return render(request, 'delete_blog_post.html', {'blog_post': blog_post})


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
