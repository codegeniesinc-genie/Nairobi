# Import necessary modules and classes
from django.views.generic.base import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, Event, Blog
from .forms import CreateUserForm, LoginForm, BlogForm, EventForm, SearchForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate 
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Event, Blog
from django.contrib.auth.models import User

# Define views
class HomePageView(TemplateView):
    template_name = 'events/homepage.html'

    def get_context_data(self, **kwargs):
        # Retrieve published events
        events = Event.objects.filter(is_published=True)
        context = {'events': events}
        return context

class EventsPageView(TemplateView):
    template_name = 'events/events.html'

    def get_context_data(self, **kwargs):
        # Retrieve published events, ordered by publication date
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
        # Retrieve blogs categorized by type, ordered by publication date
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
        # Retrieve single blog post along with related posts
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

class CheckOutPageView(TemplateView):
    template_name = 'events/checkout.html'

class PaymentPageView(TemplateView):
    template_name = 'events/payment.html'

# Define user-related views
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login/")
    
    context = {'registerform':form}

    return render(request, 'events/register.html', context=context)

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username, password=password)

            if user is not None:
                auth.login(request,user)
                return redirect("/profile/")
            
    context = {'loginform':form}

    return render(request, 'events/login.html', context=context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect("/login/")

@login_required
def profile(request):
    return render(request, 'events/profile.html')

# Define blog-related views
@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect("/blog/")
    else:
        form = BlogForm()
    return render(request,'events/create_blog.html', {'form': form})

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

# Define event-related views
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST,request.FILES)
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

    # If no users found, return no results found message
    if users.exists():
        for user in users:
            # If user found, get all blogs associated with this user
            user_blogs = Blog.objects.filter(author=user)
            context['user_blogs'] = user_blogs
            break  # Only consider the first user found

    return render(request, 'events/search_results.html', context)


@login_required
def add_to_cart(request, event_id):
    # Get the event object based on the event_id
    event = get_object_or_404(Event, pk=event_id)
    
    # Check if the event is already in the user's cart
    cart_item, created = Cart.objects.get_or_create(user=request.user, event=event)

    # If the event is already in the cart, update the quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item.save()

    # Redirect the user to the cart page or any other desired page
    return redirect('cart:cart_view')


  # You need to define the URL pattern for the cart view

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart

@login_required
def cart_view(request):
    # Retrieve all items in the cart for the current user
    cart_items = Cart.objects.filter(user=request.user)
    
    # Calculate the total price of all items in the cart
    total_price = sum(item.event.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'events/cart_view.html', context)

def checkout_view(request):
    # Retrieve the user's cart items and total price
    cart_items = request.user.cart_set.all()  # Assuming you have a Cart model associated with the user
    total_price = sum(item.event.price * item.quantity for item in cart_items)

    # Pass the cart items and total price to the checkout template
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'events/checkout.html', context)

from django.shortcuts import render
from django.http import HttpResponse

def process_payment_view(request):
    if request.method == 'POST':
        # Retrieve payment details from the form
        card_number = request.POST.get('card_number')
        expiration_date = request.POST.get('expiration_date')
        cvv = request.POST.get('cvv')
        
        # Perform payment processing logic here
        # For demonstration purposes, let's assume the payment is successful
        payment_successful = True
        
        if payment_successful:
            # Payment successful, render confirmation page
            return render(request, 'events/payment_confirmation.html')
        else:
            # Payment failed, render error page
            return render(request, 'events/payment_error.html')
    
    # If request method is not POST, return an empty response
    return HttpResponse(status=400)
