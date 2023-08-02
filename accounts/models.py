import os

from django.contrib.auth.models import AbstractUser

from django.db import models


# fmt: off
class User(AbstractUser):

    def save(self, *args, **kwargs):
        new = not self.pk
        super().save(*args, **kwargs)
        if new:
            Profile.objects.create(user_id=self.pk)

# fmt: on


class Profile(models.Model):
    def user_dir_path(self, instance=None):
        if instance:
            return os.path.join("users", str(self.pk), f"{self.user.username}-profile-img.{instance.split('.')[-1]}")
        return None

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    image = models.ImageField(upload_to=user_dir_path, blank=True, null=True, max_length=255)
    bio = models.TextField(null=True, blank=True)
