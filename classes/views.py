from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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