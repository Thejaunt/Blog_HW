from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import RegisterForm


class RegisterFormView(generic.FormView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()

        user = authenticate(self.request, username=user.username, password=form.cleaned_data.get("password1"))
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UserProfile(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = get_user_model()
    fields = ["first_name", "last_name", "email"]
    template_name = "registration/update_profile.html"
    success_url = reverse_lazy("profile")
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        user = self.request.user
        return user
