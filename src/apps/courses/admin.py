from django.contrib import admin

from src.apps.courses.models import Course, Module, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = [
        Subject.title.field.name,
        Subject.slug.field.name,
    ]
    prepopulated_fields = {
        Subject.slug.field.name: (Subject.title.field.name,),
    }


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        Course.title.field.name,
        Course.subject.field.name,
        Course.created.field.name,
    ]
    list_filter = [
        Course.created.field.name,
        Course.subject.field.name,
    ]
    search_fields = [
        Course.title.field.name,
        Course.overview.field.name,
    ]
    prepopulated_fields = {
        Course.slug.field.name: (Course.title.field.name,),
    }
    inlines = [ModuleInline]
