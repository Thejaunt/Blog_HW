from django.urls import path
from .views import create_post, home, personal_posts_view, post_detail_view, posts_list_view, update_post

app_name = "blog"
urlpatterns = [
    path("", home, name="home"),
    path("posts/", posts_list_view, name="posts"),
    path("post/<int:pk>", post_detail_view, name="post-detail"),
    path("create-post", create_post, name="create-post"),
    path("update-post/<int:pk>", update_post, name="update-post"),
    path("personal-posts/", personal_posts_view, name="personal-posts"),
]
