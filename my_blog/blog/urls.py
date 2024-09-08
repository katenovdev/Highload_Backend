from django.urls import path
from .views import *

urlpatterns = [
    path('', blog_home, name='blog_home'),
    path('get-list', post_list, name='post_list'),
    path('get/<int:id>/', post_detail, name='post_detail'),
    path('create/', post_create, name='post_create'),
    path('edit/<int:id>/', post_edit, name='post_edit'),  
    path('delete/<int:id>/', post_delete, name='post_delete'),  
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]