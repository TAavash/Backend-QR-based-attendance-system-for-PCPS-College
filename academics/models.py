from django.db import models

class Year(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Semester(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return f"Semester {self.number}"


class Section(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.code})"
