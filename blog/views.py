from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm, CustomUserCreationForm

from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')

    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk = pk)

    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk = post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk = pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance = post)
    return render(request, 'blog/post_edit.html', {'form': form})


def RegisterFormView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, 'Account created successfully')

            f_username = form.cleaned_data.get('username')
            f_password = form.cleaned_data.get('password1')
            user = auth.authenticate(username = f_username, password = f_password)
            auth.login(request, user)
            return redirect('post_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'blog/register.html', {'form': form})


def LoginFormView(request):
    if request.user.is_authenticated():
        return redirect('post_list')

    if request.method == 'POST':
        entered_username = request.POST.get('username')
        entered_password = request.POST.get('password')
        user = auth.authenticate(username = entered_username, password = entered_password)

        if user is not None:
            auth.login(request, user)
            return redirect('post_list')
        else:
            messages.error(request, 'Error: wrong username/password')

    return render(request, 'blog/login.html')

def LogoutView(request):
    auth.logout(request)
    return redirect('post_list')

'''
def admin_page(request):
    if not request.user.is_authenticated():
        return redirect('LoginFormView')

    return render(request, 'blog/admin_page.html')
'''
