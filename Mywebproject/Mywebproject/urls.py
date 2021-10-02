"""Mywebproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from Blogproject import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('admin', admin.site.urls),
    url(r'^post_list/',views.post_list,name='post_list'),
    url(r'^nthblog/(?P<id>\d+)/(?P<slug>[\w-]+)/$',views.post_detail, name='post_detail'),
    url(r'^register/',views.register_page, name='register'),
    url(r'^$',views.login_page,name='login'),
    url(r'^logout/',views.logout_page,name='logout'),
    url(r'post_create/',views.post_create,name='post_create'),
    url(r'^edit_profile/',views.edit_profile,name='edit_profile'),
    url(r'^likes/$',views.like_post, name='like_post'),
    url(r'(?P<id>\d+)/post_edit/$',views.post_edit, name='post_edit'),
    url(r'(?P<id>\d+)/post_delete/$',views.post_delete, name='post_delete'),
    url(r'(?P<id>\d+)/favourite_post/$',views.favourite_post, name='favourite_post'),
    url(r'favourites/$',views.post_favourite_list, name='post_favourite_list')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)