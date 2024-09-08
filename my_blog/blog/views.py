from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import *
from django.core.paginator import Paginator


def blog_home(request):
    return HttpResponse("Hello, Blog!")

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')  # Adjust ordering as needed
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'post_list.html', {'page_obj': page_obj})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', id=post.id)
    else:
        form = CommentForm()    
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('post_list') 
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    post_author = post.author

    current_username = request.user.username

    if current_username!=post_author:
        return redirect('post_list')  

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'post_form.html', {'form': form, 'post': post})

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    
    post_author = post.author

    current_username = request.user.username
    if post_author != current_username:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    
    return render(request, 'post_confirm_delete.html', {'post': post})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Automatically log in the user after registration
            return redirect('blog_home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('blog_home')
        else:
            # Handle invalid login
            return redirect('login')
    return render(request, 'login.html')

def user_logout(request):
    auth_logout(request)
    return redirect('blog_home')