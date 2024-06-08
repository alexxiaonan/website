"""
URL configuration for whatsapptexting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('home1/', views.home1, name='home1'),

    path('upload_image/', views.upload_image, name='upload_image'),

    path('image_similar/', views.image_similar, name='image_similar'),

    path('tag_manipulation/', views.tag_manipulation, name='tag_manipulation'),

    path('tag_search/', views.tag_search, name='tag_search'),

    path('thumbnail_full/', views.thumbnail_full, name='thumbnail_full'),

    path('delete_image/', views.delete_image, name='delete_image'),

    path('subscribe/', views.subscribe, name='subscribe'),
    
    path('logout/', views.logout_user, name='logout'),
    
    
   
]
