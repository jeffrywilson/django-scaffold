from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    # These fields allow differentiation between the different user roles:
    # is_administrator -> Administrator
    # is_manager -> Manager
    # no flag active -> Regular user
    is_administrator = models.BooleanField("administrator status", default=False)
    is_manager = models.BooleanField("manager status", default=False)
    phone = PhoneNumberField(
        unique=True, 
        verbose_name=_("Phone number"),
        null=True,
        blank=True
    )

    def set_administrator_role(self):
        self.is_manager = False
        self.is_administrator = True
        self.save()

    def set_manager_role(self):
        self.is_administrator = False
        self.is_manager = True
        self.save()

    def set_regular_role(self):
        self.is_administrator = False
        self.is_manager = False
        self.save()

    def toggle_account_status(self):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        self.save()

    def deactivate_account(self):
        self.is_active = False
        self.save()

    def activate_account(self):
        self.is_active = True
        self.save()



class Profile(models.Model):
    """
    Profile For registered User
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    profile_photo = models.ImageField(
        default='profile/profile_default.png',
        upload_to='profile',
        blank=True
    )
    cover_photo = models.ImageField(
        default='profile/cover_default.png',
        upload_to='profile',
        blank=True
    )
    bio = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
