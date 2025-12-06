from django.contrib import admin
from .models import Year, Semester, Section, Subject

@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("id", "number")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "semester")
