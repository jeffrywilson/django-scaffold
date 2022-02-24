from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, ListView, View, TemplateView, UpdateView
from django.urls import reverse_lazy, reverse


from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import RegisterView

from .decorators import AdministratorRequiredMixin, ManagerRequiredMixin
from .forms import UserInviteForm, ManagerInviteForm, ProfileUpdateForm
from .models import Profile
User = get_user_model()


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "registration/my_profile.html"


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    template_name = "registration/update_profile.html"
    model = Profile
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("my_profile")

    def get_object(self, queryset=None):
        return self.request.user.profile


class InviteRegularUser(AdministratorRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "registration/invite_user.html"
    form_class = UserInviteForm
    success_url = reverse_lazy('user_roles')
    success_message = "The user account was created successfully. An invitation has been sent to the user's email."

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['request'] = self.request
        return kwargs


class InviteManager(ManagerRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "registration/invite_manager.html"
    form_class = ManagerInviteForm
    success_url = reverse_lazy('user_roles')
    success_message = "The manager account was created successfully. An invitation has been sent to the user's email."

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['request'] = self.request
        return kwargs


class UserRoles(ManagerRequiredMixin, ListView):
    template_name = "registration/user_roles.html"
    model = User
    context_object_name = "users"


class ToggleUserAccountStatus(AdministratorRequiredMixin, View):
    model = User

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(
            self.model, id=self.kwargs.get('user_id')
        )
        user.toggle_account_status()
        return redirect("user_roles")


class ChangeUserRole(AdministratorRequiredMixin, View):
    model = User

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(self.model, id=self.kwargs.get('user_id'))
        role = self.kwargs.get('role')
        if role == "admin":
            user.set_administrator_role()
        elif role == "manager":
            user.set_manager_role()
        elif role == "regular":
            user.set_regular_role()

        return redirect("user_roles")

class CustomRegisterView(RegisterView):
    pass
