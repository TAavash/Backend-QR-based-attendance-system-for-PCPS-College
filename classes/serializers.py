from rest_framework import serializers
from .models import ClassSession, Routine

class ClassSessionSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source="subject.name", read_only=True)
    year = serializers.CharField(source="year.name", read_only=True)
    section = serializers.CharField(source="section.name", read_only=True)

    class Meta:
        model = ClassSession
        fields = ["id", "class_code", "subject", "year", "section"]
        
class AssignUsersSerializer(serializers.Serializer):
    class_id = serializers.IntegerField()
    teacher_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    student_ids = serializers.ListField(child=serializers.IntegerField(), required=False)


class RoutineSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source="class_session.subject.name", read_only=True)
    year = serializers.CharField(source="class_session.year.name", read_only=True)
    section = serializers.CharField(source="class_session.section.name", read_only=True)
    class_code = serializers.CharField(source="class_session.class_code", read_only=True)

    class Meta:
        model = Routine
        fields = ["id", "day", "start_time", "end_time", "subject", "year", "section", "class_code"]
