from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import cache_page
from django.core.cache import cache


class PostListView(View):
    def get(self, request):
        cache_key = 'post_list'
        posts = cache.get(cache_key)

        if not posts:
            posts = Post.objects.prefetch_related('comments').all()
            cache.set(cache_key, posts, 60)
        
        return render(request, 'post_list.html', {'posts': posts})

@method_decorator(login_required, name='dispatch')
class PostCreateView(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'post_form.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author to the logged-in user
            post.save()
            form.save_m2m()  # Save ManyToMany relationships
            return redirect('post_list')
        return render(request, 'post_form.html', {'form': form})

class PostDetailView(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comment_form = CommentForm()
        
        # Кешируем количество комментариев
        comments_count = cache.get(f'comments_count_{post_id}')
        if comments_count is None:
            comments_count = post.comments.count()  # Дорогой запрос
            cache.set(f'comments_count_{post_id}', comments_count, timeout=60)  # Кешируем на 60 секунд

        return render(request, 'post_detail.html', {
            'post': post,
            'comment_form': comment_form,
            'comments_count': comments_count,
        })

    @method_decorator(login_required)
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            # Инвалидируем кеш после добавления комментария
            cache.delete(f'comments_count_{post_id}')
            
            return redirect('post_detail', post_id=post.id)
class CommentCreateView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)  
        comment_form = CommentForm(request.POST)   

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user 
            comment.save() 

            cache.delete('post_list')

            return redirect('post_detail', post_id=post_id)

        return render(request, 'post_detail.html', {'post': post, 'comment_form': comment_form})

class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
        return render(request, 'register.html', {'form': form})

class UserLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
        return render(request, 'login.html', {'form': form})
