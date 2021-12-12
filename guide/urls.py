from django.urls import path
from . import views


app_name = 'guide'

urlpatterns = [
    path('', views.user_view, name='index'),
    path('map', views.default_map, name='map'),
    path('reviews/', views.ReviewsView.as_view(), name='reviews'),
    path('reviews/list', views.listR, name='listR'),
    path('request/', views.RequestView.as_view(), name='request'),
    path('request/done', views.reqList, name='reqList'),
    path('request/download', views.csvView, name='csvView'),
    path('personalize/', views.user_view, name='personalize'),
    path('thanks/', views.info_success, name='thanks'),
    path('send_sms', views.send_sms, name='send_sms'),
]
