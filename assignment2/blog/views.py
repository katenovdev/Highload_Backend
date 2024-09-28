from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm


class PostListView(View):
    def get(self, request):
        posts = Post.objects.prefetch_related('comments').all()
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
        comment_form = CommentForm()  # Initialize the form
        return render(request, 'blog/post_detail.html', {
            'post': post,
            'comment_form': comment_form,
        })

    @method_decorator(login_required)
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comment_form = CommentForm(request.POST)  # Use the request data
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user  # Set the author to the logged-in user
            comment.save()
            return redirect('post_detail', post_id=post.id)  # Redirect to post detail page
        return render(request, 'post_detail.html', {
            'post': post,
            'comment_form': comment_form,
        })

class CommentCreateView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)
        comment_form = CommentForm(request.POST)  # Use the request data
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  
            comment.save()
            return redirect('post_list')
        return render(request, 'post_detail.html', {'post': post,  'comment_form': comment_form,})

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
