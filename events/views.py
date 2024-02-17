from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Event, Blog, CartItem
from .forms import CreateUserForm, LoginForm, BlogForm, EventForm, SearchForm
from django.http import JsonResponse

class HomePageView(TemplateView):
    template_name = 'events/homepage.html'

    def get_context_data(self, **kwargs):
        events = Event.objects.filter(is_published=True)
        context = {'events': events}
        return context

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

class SinglePostView(TemplateView):
    template_name = 'events/singlePost.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_id = kwargs['blog_id']
        blog = get_object_or_404(Blog, id=blog_id)
        category = blog.category
        next_post = Blog.objects.filter(category=category, pub_date__gt=blog.pub_date).order_by('pub_date').first()
        prev_post = Blog.objects.filter(category=category, pub_date__lt=blog.pub_date).order_by('-pub_date').first()
        latest_blogs = Blog.objects.exclude(id=blog.id).order_by('-pub_date')[:5]  
        context.update({
            'blog': blog,
            'next_post': next_post,
            'prev_post': prev_post,
            'latest_blogs': latest_blogs,
        })
        return context

class SingleEventView(DetailView):
    model = Event
    template_name = 'events/singleEvents.html'
    context_object_name = 'event'

class CheckOutPageView(TemplateView):
    template_name = 'events/checkout.html'

class PaymentPageView(TemplateView):
    template_name = 'events/payment.html'

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login/")
    context = {'registerform':form}
    return render(request, 'events/register.html', context=context)

def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/profile/")
    context = {'loginform':form}
    return render(request, 'events/login.html', context=context)

@login_required
def logout_user(request):
    logout(request)
    return redirect("/login/")

@login_required
def profile(request):
    return render(request, 'events/profile.html')

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect("/blogs/")
    else:
        form = BlogForm()
    return render(request, 'events/create_blog.html', {'form': form})

@login_required
def update_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.user == blog.author:
        if request.method == 'POST':
            form = BlogForm(request.POST, instance=blog)
            if form.is_valid():
                form.save()
                return redirect("/blog/")
        else:
            form = BlogForm(instance=blog)
        return render(request, 'events/update_blog.html/', {'form': form})
    else:
        return render(request, 'events/access_denied.html/')

@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.user == blog.author:
        blog.delete()
        return redirect("/blog/")
    else:
        return render(request, 'events/access_denied.html')

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect("/events/")
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user == event.organizer:
        if request.method == 'POST':
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect('/events/')
        else:
            form = EventForm(instance=event)
        return render(request, 'events/update_event.html', {'form': form})
    else:
        return render(request, 'events/access_denied.html')

@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user == event.organizer:
        event.delete()
        return redirect('/events/')
    else:
        return render(request, 'events/access_denied.html')

def search(request):
    form = SearchForm(request.GET)
    query = None
    users = events = blogs = None

    if form.is_valid():
        query = form.cleaned_data.get('query')
        users = User.objects.filter(username__icontains=query)
        events = Event.objects.filter(
            Q(title__icontains=query) |
            Q(organizer__username__icontains=query)  
        )
        blogs = Blog.objects.filter(
            Q(title__icontains=query) |
            Q(author__username__icontains=query)  
        )

    context = {
        'form': form,
        'query': query,
        'users': users,
        'events': events,
        'blogs': blogs
    }
    
    if users.exists():
        for user in users:
            user_blogs = Blog.objects.filter(author=user)
            context['user_blogs'] = user_blogs
            break

    return render(request, 'events/search_results.html', context)

from mpesa_api.views import lipa_na_mpesa_online

def checkout(request):
    if request.method == 'POST':
        total_amount = request.POST.get('total_amount')
        user_phone_number = request.POST.get('phone_number')
        lipa_na_mpesa_online(request)
        return render(request, 'payment_processing.html')
    else:
        return render(request, 'checkout_form.html')

def payment(request):
    if request.method == 'POST':
        payment_amount = request.POST.get('amount')
        payment_method = request.POST.get('method')
        return JsonResponse({'message': 'Payment successful'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'events/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    product = Event.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('events:view_cart')

def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('events:view_cart')
