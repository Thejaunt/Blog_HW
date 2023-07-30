from django.contrib import admin

from .models import Comment, Post


class PostAdmin(admin.ModelAdmin):
    model = Post
    fields = [
        "approved",
        "title",
        "description",
    ]
    list_filter = ["is_published", "approved", "user"]
    search_fields = ["is_published", "title", "id"]
    list_display = [
        "approved",
        "is_published",
        "title",
        "description",
        "created_at",
        "updated_at",
    ]

    actions = ["make_approved", "make_unapproved"]
    from .actions import make_approved, make_unapproved


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    fields = ["is_published", "text"]
    list_display = [
        "is_published",
        "created_at",
        "updated_at",
        "text",
    ]

    actions = ["make_published", "make_unpublished"]
    from .actions import make_published, make_unpublished


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
