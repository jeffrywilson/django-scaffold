from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import Profile

class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super(AccountAdapter, self).save_user(request, user, form, commit)
        user.phone = form.cleaned_data.get("phone", None)
        user.save()
        return user

    def confirm_email(self, request, email_address):
        profile = Profile ()
        profile.user = request.user
        profile.save()
        return super().confirm_email(request, email_address)

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    pass
