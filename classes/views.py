from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from account.models import User
from .models import ClassSession
from .serializers import ClassSessionSerializer

class ClassSessionListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == "teacher":
            classes = ClassSession.objects.filter(teachers=user)
        else:
            return Response({"detail": "Unauthorized"}, status=403)

        serializer = ClassSessionSerializer(classes, many=True)
        return Response(serializer.data)
    
class AssignUsersToClassAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "admin":
            return Response({"error": "Only admin allowed"}, status=403)

        class_id = request.data.get("class_id")
        teacher_ids = request.data.get("teacher_ids", [])
        student_ids = request.data.get("student_ids", [])

        try:
            session = ClassSession.objects.get(id=class_id)
        except ClassSession.DoesNotExist:
            return Response({"error": "Class not found"}, status=404)

        # Assign teachers
        if teacher_ids:
            teachers = User.objects.filter(id__in=teacher_ids, role="teacher")
            session.teachers.set(teachers)

        # Assign students
        if student_ids:
            students = User.objects.filter(id__in=student_ids, role="student")
            session.students.set(students)

        session.save()
        return Response({
            "message": "Users assigned successfully"
        })
