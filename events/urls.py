
from django.urls import path
from .views import HomePageView,DashBoardView,EventsPageView,AboutPageView,ContactPageView,PrivacyPolicyPageView,BlogPageView,single_post,CheckOutPageView,PaymentPageView, LoadMorePostsView

app_name = 'events'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('dashboard/',DashBoardView.as_view(), name='mine_view'),
    path('events/',EventsPageView.as_view(),name='events'),
    path('about/',AboutPageView.as_view(),name='about'),
    path('contact/',ContactPageView.as_view(),name='contact'),
    path('policy/',PrivacyPolicyPageView.as_view(),name='policy'),
    path('blog/', BlogPageView.as_view(), name='blog_page'),
    path('blog/<int:blog_id>/', single_post, name='single_post'),
    path('checkout/',CheckOutPageView.as_view(),name='checkout'),
    path('payment/',PaymentPageView.as_view(),name='payment'),
    path('load_more_posts/', LoadMorePostsView.as_view(),name='more'),
]
