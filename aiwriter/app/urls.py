from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'), 
    path('website', views.website, name='website'),  
    path('api', views.OpenaiAPI, name='api'),  
    path('youtubeapi', views.YoutubeAPI, name='youtubeapi'),  
    path('bulkpost', views.bulkpost, name='bulkpost'),  
    path('singlepost', views.singlepost, name='singlepost'),  
    path('completepost', views.completepost, name='completepost'),  
    path('single_website/<website_id>', views.single_website, name='single_website'),  
    path('update_website/<website_id>', views.update_website, name='update_website'),  
    path('delete_website/<website_id>', views.delete_website, name='delete_website'),  
    path('delete_api/<api_id>', views.delete_api, name='delete_api'),  
    path('delete_youtube_api/<api_id>', views.delete_youtube_api, name='delete_youtube_api'),  
]