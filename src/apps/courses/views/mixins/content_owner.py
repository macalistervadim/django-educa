from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)


class ContentOwnerMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """
    Миксин для проверки наличия у пользователя прав на
    изменение контента
    """

    permission_required = (
        "courses.add_course",
        "courses.delete_course",
        "courses.change_course",
    )
