from django.db import models
from account.models import User
from academics.models import Subject, Year, Section

class ClassSession(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    class_code = models.CharField(max_length=50)
    teachers = models.ManyToManyField(User, limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(User, related_name="student_classes", limit_choices_to={'role': 'student'}, blank=True)


    def __str__(self):
        return f"{self.subject.name} - {self.class_code}"


class Routine(models.Model):
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)  # Monday, Tuesday...
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day} - {self.class_session.class_code}"
