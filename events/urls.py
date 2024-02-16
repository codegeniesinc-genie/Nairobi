from django.urls import  path
from . import views
from .views import HomePageView,EventsPageView,AboutPageView,ContactPageView,PrivacyPolicyPageView,BlogPageView, SinglePostView,CheckOutPageView,PaymentPageView

app_name = 'events'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('events/',EventsPageView.as_view(),name='events'),
    path('events/create', views.create_event, name='create_event'),
    path('events/update/<int:pk>/', views.update_event, name='update_event'),
    path('events/delete/<int:pk>/', views.delete_event, name='delete_event'),
    path('blogs/', BlogPageView.as_view(), name='blog_page'),
    path('blogs/blog/<int:blog_id>/', SinglePostView.as_view(), name='single_post'),
    path('blogs/create', views.create_blog, name='create_blog'),
    path('blogs/update/<int:pk>/', views.update_blog, name='update_blog'),
    path('blogs/delete/<int:pk>/', views.delete_blog, name='delete_blog'),
    path('about/',AboutPageView.as_view(),name='about'),
    path('contact/',ContactPageView.as_view(),name='contact'),
    path('policy/',PrivacyPolicyPageView.as_view(),name='policy'),
    path('checkout/',CheckOutPageView.as_view(),name='checkout'),
    path('payment/',PaymentPageView.as_view(),name='payment'),
    path('register/',views.register, name='register'),
    path('login/',views.login,name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout,name='logout'),
    path('search/', views.search, name='search_results'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout_view, name='checkout_view'),
    path('process_payment/', views.process_payment_view, name='process_payment'),
]
