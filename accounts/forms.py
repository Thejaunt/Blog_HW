import imghdr

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from accounts.models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        exists = get_user_model().objects.filter(email=email)
        if exists.count():
            raise ValidationError("email already exists")
        return email


class ProfileImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={"class": "form-control"}))

    class Meta:
        model = Profile
        fields = ("image",)

    def clean_profile_img(self):
        image_types = {
            "jpeg": "image/jpeg",
            "jpg": "image/jpeg",
            "png": "image/png",
        }
        img_max_size = 1048576  # about 1Mb
        img = self.cleaned_data.get("image")
        if img is None:
            return img

        if img.size > img_max_size:
            raise ValidationError("The file is too big.")

        img_extension = img.name.split(".")[-1]
        if not img_extension or img_extension.lower() not in image_types.keys():
            raise ValidationError("Wrong extension of the image")

        mime_type = imghdr.what(img)
        if mime_type not in image_types.keys():
            raise ValidationError("Wrong mime-type of the image")

        return img


class ProfileBioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio",)
