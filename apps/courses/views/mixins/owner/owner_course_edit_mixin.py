from apps.courses.views.mixins.owner import OwnerCourseMixin, OwnerEditMixin


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
    Миксин для редактирования курсов, принадлежащих конкретному пользователю.
    """

    template_name = "courses/manage/course/form.html"
