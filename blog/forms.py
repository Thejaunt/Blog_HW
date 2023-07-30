from django import forms

from .models import Comment, Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["is_published", "title", "description"]


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["is_published", "title", "description"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class ContactForm(forms.Form):
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea())
