from django.urls import  path
from . import views
from .views import HomePageView,EventsPageView,AboutPageView,ContactPageView,PrivacyPolicyPageView,BlogPageView, SingleEventView, SinglePostView,CheckOutPageView,PaymentPageView

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
    path('accounts/register/',views.register, name='register'),
    path('accounts/login/',views.login,name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/logout/', views.logout,name='logout'),
    path('search/', views.search, name='search_results'),  
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
