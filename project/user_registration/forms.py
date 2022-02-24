from django import forms
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.urls import reverse

from allauth.utils import build_absolute_uri
from allauth.account.adapter import get_adapter
from allauth.account.forms import default_token_generator
from allauth.account.models import EmailAddress
from allauth.account.utils import filter_users_by_email, user_pk_to_url_str

from .models import Profile

USER = get_user_model()


class UserInviteForm(forms.ModelForm):
    class Meta:
        model = get_user_model()

        fields = ["email"]

        widgets = {
            "email": forms.EmailInput(attrs={"class": "validate", "type": "email"})
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserInviteForm, self).__init__(*args, **kwargs)
        self.fields["email"].required = True

    def clean_email(self):
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email)
        if self.users:
            raise forms.ValidationError(
                "This email address is already in use by another user."
            )
        return email

    @transaction.atomic
    def save(self, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data["email"]
        user.username = email.split("@")[0]
        user.save()
        self._set_user_role(user=user)
        EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)
        self._send_invitation_link(user=user, request=self.request)
        return user

    def _set_user_role(self, user):
        """
        Override this function to assign a role to the user
        E.g: user.is_manager = True OR user.set_manager_role()
        Default: Regular User template and settings
        """
        pass

    def get_template_prefix(self):
        """
        Obtain the string with the template prefix to use in the emails.
        Override this function to assign another template prefix
        """
        return "registration/email/invited_user"

    def _send_invitation_link(self, user, request, **kwargs):
        """
        Send a link to the user after being invited to the site
        to reset the password when clicked. (Using allauth patterns)
        """
        current_site = get_current_site(request)
        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator", default_token_generator)

        temp_key = token_generator.make_token(user)
        # send the password reset email
        path = reverse(
            "account_reset_password_from_key",
            kwargs=dict(uidb36=user_pk_to_url_str(user), key=temp_key),
        )
        url = build_absolute_uri(request, path)

        context = {
            "current_site": current_site,
            "user": user,
            "password_reset_url": url,
            "request": request,
        }

        get_adapter(request).send_mail(self.get_template_prefix(), email, context)


class ManagerInviteForm(UserInviteForm):
    def get_template_prefix(self):
        return "registration/email/invited_manager"

    def _set_user_role(self, user):
        user.set_manager_role()


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = Profile
        fields = [
            'profile_photo',
            'cover_photo',
            'first_name',
            'last_name', 
            'bio'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.pk:
            profile = instance
            self.initial["first_name"] = profile.user.first_name
            self.initial["last_name"] = profile.user.last_name
            self.initial["profile_photo"] = profile.profile_photo
            self.initial["cover_photo"] = profile.cover_photo
            self.initial["bio"] = profile.bio

    def save(self, *args, **kwargs):
        profile =  self.instance

        profile.user.first_name = self.cleaned_data["first_name"]
        profile.user.last_name = self.cleaned_data["last_name"]
        user = profile.user
        user.save()
        
        profile.profile_photo = self.cleaned_data["profile_photo"]
        profile.cover_photo = self.cleaned_data["cover_photo"]
        profile.bio = self.cleaned_data["bio"]
        profile = super(ProfileUpdateForm, self).save()
        profile.save()
        return profile

