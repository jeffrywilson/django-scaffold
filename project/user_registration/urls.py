from django.urls import path, re_path, include

from .views import (
    InviteManager,
    InviteRegularUser,
    UserRoles,
    ToggleUserAccountStatus,
    ChangeUserRole,
    ProfileView,
    UpdateProfileView,
    CustomRegisterView,
)

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('profile/', ProfileView.as_view(), name='my_profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    # Dashboard Urls
    path("registration/invite-users/", InviteRegularUser.as_view(), name="invite_users"),
    path("registration/invite-managers/", InviteManager.as_view(), name="invite_managers"),
    path("registration/user-roles/", UserRoles.as_view(), name="user_roles"),
    path(
        "registration/users-roles/<int:user_id>/toggle-account-status/",
        ToggleUserAccountStatus.as_view(),
        name="toggle_account_status",
    ),
    path(
        "registration/users-roles/<int:user_id>/assign/<str:role>/",
        ChangeUserRole.as_view(),
        name="change_user_role",
    ),
]

api_patterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/register/", CustomRegisterView.as_view(), name='register'),
]
