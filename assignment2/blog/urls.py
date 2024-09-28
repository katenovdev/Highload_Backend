from django.urls import path
from .views import *

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:post_id>/comments/create/', CommentCreateView.as_view(), name='comment_create'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
]