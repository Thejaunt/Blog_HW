from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CreatePostForm, UpdatePostForm
from .models import Comment, Post


def home(request):
    return render(request, "home.html")


def posts_list_view(request):
    objs = Post.objects.filter(approved=True, is_published=True).prefetch_related("user")
    paginator = Paginator(objs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/posts.html", {"page_obj": page_obj, "is_paginated": True})


@login_required
def personal_post_detail_view(request, pk):
    obj = get_object_or_404(
        Post.objects.prefetch_related(
            Prefetch("comment_set", queryset=Comment.objects.filter(is_published=True).select_related("user"))
        ),
        pk=pk,
        user=request.user,
    )
    com_count = obj.comment_set.count()
    paginator = Paginator(obj.comment_set.all(), 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    is_creator = False
    if request.user == obj.user:
        is_creator = True
    context = {"obj": obj, "com_count": com_count, "is_creator": is_creator, "is_paginated": True, "page_obj": page_obj}
    return render(request, "blog/personal-post-detail.html", context)


def post_detail_view(request, pk):
    obj = get_object_or_404(
        Post.objects.prefetch_related(
            Prefetch("comment_set", queryset=Comment.objects.filter(is_published=True).select_related("user"))
        ),
        is_published=True,
        approved=True,
        pk=pk,
    )
    com_count = obj.comment_set.count()
    paginator = Paginator(obj.comment_set.all(), 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    is_creator = False
    if request.user == obj.user:
        is_creator = True

    context = {"obj": obj, "com_count": com_count, "is_creator": is_creator, "is_paginated": True, "page_obj": page_obj}
    return render(request, "blog/post-detail.html", context)


@login_required
def create_post(request):
    form = CreatePostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data.get("title")
            description = form.cleaned_data.get("description")
            is_published = form.cleaned_data.get("is_published")
            post = Post(user=request.user, title=title, description=description, is_published=is_published)
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
def delete_post_view(request, pk):
    obj = get_object_or_404(Post, pk=pk, user=request.user)
    if request.method == "POST" and request.user == obj.user:
        obj.delete()
        return redirect("blog:personal-posts")
    return render(request, "blog/delete-post.html", {"obj": obj})


@login_required
def personal_posts_view(request):
    objs = Post.objects.filter(user=request.user)
    return render(request, "blog/personal-posts.html", {"objs": objs})
