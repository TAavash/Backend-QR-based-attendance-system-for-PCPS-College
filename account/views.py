from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User
from account.serializers import AdminCreateUserSerializer, PasswordChangeSerializer, ProfileSerializer

class LoginAPIView(APIView):

    def post(self, request):
        uid = request.data.get('uid')
        password = request.data.get('password')

        user = User.objects.filter(uid=uid).first()

        if not user or not user.check_password(password):
            return Response({"error": "Invalid UID or password"}, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "uid": user.uid,
                "username": user.username,
                "role": user.role
            }
        })

class AdminCreateUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "admin":
            return Response({"error": "Only admins allowed"}, status=403)

        serializer = AdminCreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"})
        return Response(serializer.errors, status=400)

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ProfileSerializer(request.user).data)

class UpdateProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated"})
        return Response(serializer.errors, status=400)

class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = PasswordChangeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        old_pw = serializer.validated_data["old_password"]
        new_pw = serializer.validated_data["new_password"]

        if not request.user.check_password(old_pw):
            return Response({"error": "Old password incorrect"}, status=400)

        request.user.set_password(new_pw)
        request.user.save()

        return Response({"message": "Password changed successfully"})
