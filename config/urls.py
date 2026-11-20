from django.contrib import admin
from django.urls import path, include
from social import views as v
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', v.register, name='register'),
    path('', v.feed, name='feed'),
    path('people/', v.people, name='people'),
    path('like/<int:pk>/', v.like, name='like'),
    path('comment/<int:pk>/', v.comment, name='comment'),
    path('u/<str:username>/', v.profile, name='profile'),
    path('u/<str:username>/follow/', v.follow, name='follow'),
    path('bio/', v.edit_bio, name='bio'),
]
