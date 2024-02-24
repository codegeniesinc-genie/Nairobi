from django.urls import  path
from . import views
from .views import AuthorProfileView, CheckoutView, HomePageView,EventsPageView,AboutPageView,ContactPageView,PrivacyPolicyPageView,BlogPageView,SinglePostView

app_name = 'events'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('events/',EventsPageView.as_view(),name='events'),
    path('events/<int:id>/', views.event_single, name='eventSingle'),
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
    path('accounts/login/',views.login_user,name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/update/', views.profile_update, name='profile_update'),
    path('accounts/logout/', views.logout_user,name='logout'),
    path('search/', views.search, name='search_results'),  
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('removeone/<int:item_id>/',views.removeone_from_cart,name='removeone_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('receipt/<int:event_id>/', views.receipt, name='receipt'),
    path('event/<int:event_id>/receipt/', views.generate_receipt_pdf, name='generate_receipt_pdf'),
    path('author/<int:author_id>/', AuthorProfileView.as_view(), name='author_profile'),

]
