from django.contrib import admin, messages
from django.utils.translation import ngettext


#  POSTS
@admin.action(description="Mark selected comments as approved")
def make_approved(self, request, queryset):
    updated = queryset.update(approved=True)
    self.message_user(
        request,
        ngettext(
            "%d post was successfully marked as approved.",
            "%d posts were successfully marked as approved.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


@admin.action(description="Mark selected comments as unapproved")
def make_unapproved(self, request, queryset):
    updated = queryset.update(approved=False)
    self.message_user(
        request,
        ngettext(
            "%d post was successfully marked as unapproved.",
            "%d posts were successfully marked as unapproved.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


# COMMENTS
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
    updated = queryset.update(is_published=False)
    self.message_user(
        request,
        ngettext(
            "%d comment was successfully marked as unpublished.",
            "%d comments were successfully marked as unpublished.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )
