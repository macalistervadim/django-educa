from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


class StudentRegistrationView(CreateView):
    template_name = "students/student/registration.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("students:student_course_list")

    def form_valid(self, form: UserCreationForm) -> HttpResponse:
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd["username"], password=cd["password1"])
        login(self.request, user)
        return result
