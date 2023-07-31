from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render

from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import RegisterForm, ProfileImageForm, ProfileBioForm
from accounts.models import Profile


class RegisterFormView(generic.FormView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("blog:home")

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


@login_required
def update_profile_img(request):
    prof = Profile.objects.filter(user=request.user.pk).last()
    if not prof:
        prof = Profile.objects.create(user=request.user)
    form = ProfileImageForm(request.POST or None, request.FILES or None, instance=prof)
    if request.method == "POST":
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, "Profile image has been updated")
            else:
                messages.success(request, "Profile image hasn't been changed")
            return redirect("profile")
    return render(request, "registration/update_profile_img.html", {"form": form})


@login_required
def update_profile_bio(request):
    prof = Profile.objects.filter(user=request.user.pk).last()
    if not prof:
        prof = Profile.objects.create(user=request.user)
    form = ProfileBioForm(request.POST or None, instance=prof)
    if request.method == "POST":
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, "Profile bio has been updated")
            else:
                messages.success(request, "Profile bio hasn't been changed")
            return redirect("profile")
    return render(request, "registration/update_profile_img.html", {"form": form})
