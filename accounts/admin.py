from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Profile


class ProfileInline(admin.TabularInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]
    search_fields = ["username", "email"]
    model = get_user_model()
    fields = [
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    list_display = [
        "username",
        "email",
        "date_joined",
        "last_login",
        "is_active",
        "is_staff",
        "is_superuser",
    ]


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    fields = ["user", "bio", "image"]
    list_display = ["user", "bio", "image"]
    search_fields = ["user__username", "user__email", "bio"]


admin.site.register(get_user_model(), UserAdmin)
admin.site.register(Profile, ProfileAdmin)
