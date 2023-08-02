from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page

from .forms import CreatePostForm, ContactForm, CommentForm, UpdatePostForm
from .models import Comment, Post
from .tasks import email_contact_task


def home(request):
    return render(request, "home.html")


@cache_page(timeout=20)
def public_profile(request, username):
    ob = Post.objects.filter(is_published=True)
    objs = (
        get_user_model()
        .objects.select_related("profile")
        .prefetch_related(Prefetch("post_set", queryset=ob))
        .get(username=username)
    )
    return render(request, "blog/public-profile.html", {"objs": objs})


@login_required
def personal_posts_view(request):
    _filter = request.GET.get("filter") or "all"
    objs = Post.objects.filter(user=request.user)
    if _filter == "published":
        objs = Post.objects.filter(user=request.user, is_published=True)
    if _filter == "unpublished":
        objs = Post.objects.filter(user=request.user, is_published=False)

    return render(request, "blog/personal-posts.html", {"objs": objs})


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


@cache_page(timeout=20)
def posts_list_view(request):
    objs = Post.objects.filter(approved=True, is_published=True).select_related("user", "user__profile")
    paginator = Paginator(objs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/posts.html", {"page_obj": page_obj, "is_paginated": True})


def post_detail_view(request, pk):
    obj = get_object_or_404(
        Post.objects.prefetch_related(
            Prefetch("comment_set", queryset=Comment.objects.filter(is_published=True).select_related("user"))
        ),
        is_published=True,
        # approved=True,
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

    form = CommentForm(request.POST or None)
    context["form"] = form
    if request.method == "POST":
        if form.is_valid():
            user = request.user
            text = form.cleaned_data.get("text")

            if user.is_anonymous:
                com = Comment(post=obj, text=text)
            else:
                com = Comment(user=user, post=obj, text=text)
            if request.user.is_superuser:
                com.is_published = True
            com.save()
            context["form"] = CommentForm()
            if not request.user.is_superuser:
                messages.success(
                    request, "New Comment has been added. \n It will be shown in comments section after verification"
                )
            return redirect("blog:post-detail", obj.pk)

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
            return redirect("blog:personal-post-detail", post.pk)
    return render(request, "blog/create-post.html", {"form": form})


@login_required
def update_post(request, pk):
    obj = get_object_or_404(Post, pk=pk, user=request.user)
    form = UpdatePostForm(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            if form.has_changed():
                form.save(commit=False)
                obj.approved = False
                form.save()
                messages.success(request, "The post has been updated. And Under admins review")
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


def contact_us(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            subject = "Hallo Admin"
            from_email = settings.EMAIL_HOST
            user_email = form.cleaned_data.get("email")
            recipients = [
                str(get_user_model().objects.filter(is_superuser=True, is_active=True).first().email),
            ]
            text = form.cleaned_data.get("text")
            email_contact_task.apply_async(
                (
                    user_email,
                    subject,
                    text,
                    from_email,
                    recipients,
                ),
            )
            messages.success(request, "Your message has been successfully sent to admin")
            return redirect("blog:home")
    return render(request, "blog/contact-us.html", {"form": form})
