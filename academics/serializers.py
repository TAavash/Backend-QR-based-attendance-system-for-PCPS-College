from rest_framework import serializers
from .models import Year, Semester, Section, Subject

class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = "__all__"

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = "__all__"

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"
