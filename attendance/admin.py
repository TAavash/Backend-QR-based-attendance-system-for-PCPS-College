from django.contrib import admin
from .models import Attendance, AttendanceQRCode

@admin.register(AttendanceQRCode)
class AttendanceQRCodeAdmin(admin.ModelAdmin):
    list_display = ("uuid", "class_session", "expire_time")
    list_filter = ("class_session",)
    search_fields = ("uuid", "class_session__class_code")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "class_session", "date", "present")
    list_filter = ("class_session", "date", "present")
    search_fields = ("student__username", "class_session__class_code")
