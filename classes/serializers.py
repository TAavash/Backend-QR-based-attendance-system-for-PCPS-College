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

class CreateClassSessionSerializer(serializers.ModelSerializer):
    teacher_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    student_ids = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta:
        model = ClassSession
        fields = ["subject", "year", "section", "class_code", "teacher_ids", "student_ids"]

    def create(self, validated_data):
        teacher_ids = validated_data.pop("teacher_ids", [])
        student_ids = validated_data.pop("student_ids", [])

        session = ClassSession.objects.create(**validated_data)

        # Add teachers
        if teacher_ids:
            session.teachers.set(teacher_ids)

        # Add students
        if student_ids:
            session.students.set(student_ids)

        return session
