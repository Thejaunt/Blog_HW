from django.contrib.auth import get_user_model
from django.db import models
from core import settings
from django.urls import reverse
from .tasks import email_new_record

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    approved = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("blog:post-detail", args=[str(self.pk)])

    def save(self, *args, **kwargs):
        new = not self.pk
        super().save(*args, **kwargs)

        if new:
            if self.user.is_superuser:
                return
            subject = "New post"
            if self.user is not None:
                user = self.user.username
            else:
                user = "Anonymous"
            from_email = settings.EMAIL_HOST
            admin_url = reverse("admin:blog_post_change", args=(self.pk,))
            recipients = list(set([str(us.email) for us in User.objects.filter(is_superuser=True)]))
            text = f"""
            New Post - title: {self.title} has been added by {user} \n
            admin link: {settings.SITE_HOST}{admin_url}\n
            site link: {settings.SITE_HOST}{self.get_absolute_url()} \n"""
            email_new_record.apply_async(
                (
                    subject,
                    text,
                    from_email,
                    recipients,
                ),
            )


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    text = models.TextField(max_length=100)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        new = not self.pk
        super().save(*args, **kwargs)

        if new:
            subject = "New comment"
            if self.user is not None:
                user = self.user.username
                if self.user.is_superuser:
                    return
            else:
                user = "Anonymous"

            from_email = settings.EMAIL_HOST
            admin_url = reverse("admin:blog_comment_change", args=(self.pk,))
            recipients = list(
                set([*[str(u.email) for u in User.objects.filter(is_superuser=True)], self.post.user.email])
            )
            text = (
                f"New comment for Post title:{self.post.title},\n"
                f"admin link: {settings.SITE_HOST}{admin_url}\n"
                f"site link: {settings.SITE_HOST}{self.post.get_absolute_url()}\n"
                f"has been added by {user} user"
            )

            email_new_record.apply_async(
                (
                    subject,
                    text,
                    from_email,
                    recipients,
                ),
            )
