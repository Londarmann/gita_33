from django.shortcuts import render, redirect

from .forms import AddPostForm
from .models import Post


# Create your views here.
def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'all_post.html', {"posts": posts})


def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_post')

    else:
        form = AddPostForm()
    return render(request, 'add_post.html', {'form': form})


def delete_post(request, post_id):
    if request.method == 'POST':
        Post.objects.get(id=post_id).delete()
    return redirect('all_post')


def detail_post(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'detailed_post.html', {'detailed_post': post})


def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = AddPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('detail_post', post_id=post.id)
    else:
        form = AddPostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

