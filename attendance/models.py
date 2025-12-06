from django.db import models
from classes.models import ClassSession
from account.models import User
import uuid

class AttendanceQRCode(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    expire_time = models.DateTimeField()

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    present = models.BooleanField(default=False)
