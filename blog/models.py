from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.template import loader
from core import settings

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=70)
    description = models.TextField(max_length=500)
    approved = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("blog:post-detail", args=[str(self.pk)])

    def save(self, *args, **kwargs):
        new = not self.pk
        super().save(*args, **kwargs)

        if new:
            subject = "New post"
            if self.user is not None:
                user = self.user.username
            else:
                user = "Anonymous"
            from_email = settings.EMAIL_HOST
            recipients = set(us.email for us in User.objects.filter(is_superuser=True))
            text = f"New Post: title: '{self.title}' has been added by '{user}' user"
            message = loader.render_to_string("blog/email_comment.html", {"message": text})
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipients,
                fail_silently=False,
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
        ordering = ("created_at",)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        new = not self.pk
        super().save(*args, **kwargs)

        if new:
            subject = "New comment"
            if self.user is not None:
                user = self.user.username
            else:
                user = "Anonymous"

            from_email = settings.EMAIL_HOST
            recipients = set([*[su.email for su in User.objects.filter(is_superuser=True)], self.post.user.email])
            text = (
                f"New comment for Post title:{self.post.title},\n"
                f"link: {settings.SITE_HOST}{self.post.get_absolute_url()}\n"
                f"has been added by {user} user"
            )
            message = loader.render_to_string("blog/email_comment.html", {"message": text})
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipients,
                fail_silently=False,
            )
