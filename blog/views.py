from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CreatePostForm, UpdatePostForm
from .models import Comment, Post


def home(request):
    return render(request, "home.html")


def posts_list_view(request):
    objs = Post.objects.filter(approved=True, is_published=False).prefetch_related("user")
    return render(request, "blog/posts.html", {"objs": objs})


def post_detail_view(request, pk):
    obj = get_object_or_404(
        Post.objects.prefetch_related(
            Prefetch("comment_set", queryset=Comment.objects.filter(is_published=False).select_related("user"))
        ),
        is_published=False,
        approved=True,
        pk=pk,
    )
    com_count = obj.comment_set.count()
    is_creator = False
    if request.user == obj.user:
        is_creator = True

    return render(request, "blog/post-detail.html", {"obj": obj, "com_count": com_count, "is_creator": is_creator})


@login_required
def create_post(request):
    form = CreatePostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data.get("title")
            description = form.cleaned_data.get("description")
            post = Post(user=request.user, title=title, description=description)
            post.save()
            messages.success(request, "New post has been created")
        return redirect("blog:post-detail", post.pk)
    return render(request, "blog/create-post.html", {"form": form})


@login_required
def update_post(request, pk):
    obj = get_object_or_404(Post, pk=pk, user=request.user)
    form = UpdatePostForm(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, "The post has been updated")
            else:
                messages.success(request, "The post hasn't been changed")
        return redirect("blog:post-detail", obj.pk)
    return render(request, "blog/update-post.html", {"form": form})


@login_required
def personal_posts_view(request):
    objs = Post.objects.filter(user=request.user)
    return render(request, "blog/personal-posts.html", {"objs": objs})
