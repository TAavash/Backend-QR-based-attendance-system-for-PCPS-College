from django.db import models
from account.models import User
from academics.models import Subject, Year, Section

class ClassSession(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    class_code = models.CharField(max_length=50)
    teachers = models.ManyToManyField(User, limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return f"{self.subject.name} - {self.class_code}"
