from django.urls import include, path

from accounts.views import RegisterFormView, UpdateProfile, UserProfile

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", RegisterFormView.as_view(), name="register"),
    path("profile/", UserProfile.as_view(), name="profile"),
    path("update_profile", UpdateProfile.as_view(), name="update_profile"),
]
