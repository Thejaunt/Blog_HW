from django.urls import include, path

from accounts.views import RegisterFormView, UpdateProfile, UserProfile, update_profile_img, update_profile_bio

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", RegisterFormView.as_view(), name="register"),
    path("profile/", UserProfile.as_view(), name="profile"),
    path("update_profile", UpdateProfile.as_view(), name="update_profile"),
    path("profile/update_profile_img", update_profile_img, name="profile_img_update"),
    path("profile/update_profile_bio", update_profile_bio, name="profile_bio_update"),
]
