from django.contrib import admin

from .models import Comment, Post


class CommentInline(admin.TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    model = Post

    fields = [
        "approved",
        "title",
        "description",
    ]
    list_filter = ["is_published", "approved", "user"]
    search_fields = ["is_published", "title", "id", "approved", "user__username"]
    list_display = [
        "approved",
        "is_published",
        "title",
        "created_at",
        "updated_at",
        "user",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("comment_set")

    from .actions import make_approved, make_unapproved

    actions = [make_approved, make_unapproved]


class CommentAdmin(admin.ModelAdmin):
    # inlines = [PostAdmin]
    model = Comment
    fields = ["is_published", "text"]
    search_fields = ["is_published"]
    list_display = [
        "is_published",
        "created_at",
        "updated_at",
        "post",
        "text",
        "user",
    ]

    from .actions import make_published, make_unpublished

    actions = [make_published, make_unpublished]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
