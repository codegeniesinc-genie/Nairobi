from django.urls import path
from . import views
from .views import HomePageView,EventsPageView,AboutPageView,ContactPageView,PrivacyPolicyPageView,BlogPageView,single_post,CheckOutPageView,PaymentPageView

app_name = 'events'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('events/',EventsPageView.as_view(),name='events'),
    path('blog/', BlogPageView.as_view(), name='blog_page'),
    path('blog/<int:blog_id>/', single_post, name='single_post'),
    path('about/',AboutPageView.as_view(),name='about'),
    path('contact/',ContactPageView.as_view(),name='contact'),
    path('policy/',PrivacyPolicyPageView.as_view(),name='policy'),
    path('checkout/',CheckOutPageView.as_view(),name='checkout'),
    path('payment/',PaymentPageView.as_view(),name='payment'),
    path('register/',views.register, name='register'),
    path('login/',views.login,name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout', views.logout,name='logout')
]
