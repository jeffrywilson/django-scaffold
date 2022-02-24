from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class AdministratorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Decorator for class based views that checks that the logged in user is an Administrator or
    a SuperUser, raises 403 Error if error otherwise.
    """

    def test_func(self):
        return self.request.user.is_active and (
                self.request.user.is_superuser or self.request.user.is_administrator)


class ManagerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Decorator for class based views that checks that the logged in user is a Manager, administrator or
    a SuperUser, raises 403 Error if error otherwise.
    """

    def test_func(self):
        return self.request.user.is_active and (
                self.request.user.is_manager or
                self.request.user.is_administrator or
                self.request.user.is_superuser)

