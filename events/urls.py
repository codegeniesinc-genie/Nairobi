
from django.urls import path
from . import views
from .views import HomePageView,EventsPageView,AboutPageView,ContactPageView,PrivacyPolicyPageView,BlogPageView,single_post,CheckOutPageView,PaymentPageView

app_name = 'events'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('events/',EventsPageView.as_view(),name='events'),
    path('about/',AboutPageView.as_view(),name='about'),
    path('contact/',ContactPageView.as_view(),name='contact'),
    path('policy/',PrivacyPolicyPageView.as_view(),name='policy'),
    path('blog/', BlogPageView.as_view(), name='blog_page'),
    path('blog/<int:blog_id>/', single_post, name='single_post'),
    path('checkout/',CheckOutPageView.as_view(),name='checkout'),
    path('payment/',PaymentPageView.as_view(),name='payment'),
     path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('event/create/', views.create_event, name='create_event'),
    path('event/<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('event/<int:pk>/delete/', views.delete_event, name='delete_event'),
    path('blog/create/', views.create_blog_post, name='create_blog_post'),
    path('blog/<int:pk>/edit/', views.edit_blog_post, name='edit_blog_post'),
    path('blog/<int:pk>/delete/', views.delete_blog_post, name='delete_blog_post'),
]
