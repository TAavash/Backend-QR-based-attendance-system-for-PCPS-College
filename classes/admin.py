from django.contrib import admin
from .models import ClassSession

@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "year", "section", "class_code")
    list_filter = ("year", "section", "subject")
    search_fields = ("class_code", "subject__name")
    filter_horizontal = ("teachers",)
