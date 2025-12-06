from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from attendance.serializers import AttendanceSerializer
from classes.models import ClassSession
from attendance.models import AttendanceQRCode, Attendance
import uuid, qrcode, base64
from io import BytesIO
from datetime import datetime, timedelta

class GenerateQRCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "teacher":
            return Response({"error": "Only teachers allowed"}, status=403)

        class_id = request.data.get("class_id")
        class_session = ClassSession.objects.filter(id=class_id).first()

        if not class_session:
            return Response({"error": "Invalid class id"}, status=400)

        qr_uuid = uuid.uuid4()
        expire_time = datetime.now() + timedelta(minutes=60)

        AttendanceQRCode.objects.create(
            uuid=qr_uuid,
            class_session=class_session,
            expire_time=expire_time
        )

        qr = qrcode.make(str(qr_uuid))
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_img_base64 = base64.b64encode(buffer.getvalue()).decode()

        return Response({
            "uuid": str(qr_uuid),
            "qr_image": f"data:image/png;base64,{qr_img_base64}",
            "expires_at": expire_time
        })


class MarkAttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "student":
            return Response({"error": "Only students allowed"}, status=403)

        qr_uuid = request.data.get("qr_uuid")
        try:
            qr = AttendanceQRCode.objects.get(uuid=qr_uuid)
        except AttendanceQRCode.DoesNotExist:
            return Response({"error": "Invalid QR Code"}, status=400)

        # FIXED — use timezone.now()
        if qr.expire_time < timezone.now():
            return Response({"error": "QR expired"}, status=400)

        Attendance.objects.update_or_create(
            student=request.user,
            class_session=qr.class_session,
            date=timezone.now().date(),
            defaults={"present": True}
        )

        return Response({"success": True, "message": "Attendance marked"})

class ViewAttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "teacher" and request.user.role != "admin":
            return Response({"error": "Only teachers allowed"}, status=403)

        # Query params
        year = request.query_params.get("year")
        semester = request.query_params.get("semester")
        subject = request.query_params.get("subject")
        section = request.query_params.get("section")
        date_str = request.query_params.get("date")

        # Validate date
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        # Base query: Only teacher's classes
        class_sessions = ClassSession.objects.filter(teacher=request.user)

        # Apply filters only if provided
        if year:
            class_sessions = class_sessions.filter(year=year)

        if semester:
            class_sessions = class_sessions.filter(semester=semester)

        if subject:
            class_sessions = class_sessions.filter(subject__icontains=subject)

        if section:
            class_sessions = class_sessions.filter(section__icontains=section)

        # If no class matched
        if not class_sessions.exists():
            return Response({"error": "No class found for given filters."}, status=404)

        # Get attendance
        attendance_records = Attendance.objects.filter(
            class_session__in=class_sessions,
            date=date
        ).select_related('student', 'class_session')

        attendance_list = [
            {
                "student_id": r.student.id,
                "student_name": r.student.get_full_name(),
                "present": r.present,
                "class_session_id": r.class_session.id,
                "year": r.class_session.year,
                "semester": r.class_session.semester,
                "subject": r.class_session.subject,
                "section": r.class_session.section,
            }
            for r in attendance_records
        ]

        return Response({
            "filters": {
                "year": year,
                "semester": semester,
                "subject": subject,
                "section": section,
                "date": date
            },
            "attendance": attendance_list
        })

class StudentHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "student":
            return Response({"error": "Only students allowed"}, status=403)

        attendance = Attendance.objects.filter(student=request.user)
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)
