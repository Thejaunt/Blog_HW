from django import forms

from .models import Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["is_published", "title", "description"]


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["is_published", "title", "description"]
