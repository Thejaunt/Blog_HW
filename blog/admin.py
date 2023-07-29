from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Comment, Post


class PostAdmin(admin.ModelAdmin):
    model = Post
    fields = [
        "approved",
        "title",
        "description",
    ]
    list_display = [
        "approved",
        "is_published",
        "title",
        "description",
        "created_at",
        "updated_at",
    ]


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    fields = ["is_published"]
    list_display = [
        "is_published",
        "created_at",
        "updated_at",
        "text",
    ]

    actions = ["make_published", "make_unpublished"]

    @admin.action(description="Mark selected comments as published")
    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(
            request,
            ngettext(
                "%d story was successfully marked as published.",
                "%d stories were successfully marked as published.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description="Mark selected comments as unpublished")
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=True)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
