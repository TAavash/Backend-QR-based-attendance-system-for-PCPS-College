from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from attendance.constants import COLLEGE_LAT, COLLEGE_LNG, DEV_MODE, GEOFENCE_RADIUS_METERS
from attendance.serializers import AttendanceSerializer
from attendance.utils import decrypt_token, distance_m, encrypt_token
from classes.models import ClassSession
from attendance.models import AttendanceQRCode, Attendance
import uuid, qrcode, base64
from io import BytesIO
from datetime import timedelta


class GenerateQRCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "teacher":
            return Response({"error": "Only teachers allowed"}, status=403)

        class_id = request.data.get("class_id")
        class_session = ClassSession.objects.filter(id=class_id).first()

        if not class_session:
            return Response({"error": "Invalid class id"}, status=400)

        # Generate REAL UUID
        real_uuid = str(uuid.uuid4())

        # Encrypt the UUID (this is what student scans)
        encrypted_uuid = encrypt_token(real_uuid)

        # Expire time (timezone-aware)
        expire_time = timezone.now() + timedelta(minutes=2)

        # Save REAL UUID (NOT encrypted) into database
        AttendanceQRCode.objects.create(
            uuid=real_uuid,
            class_session=class_session,
            expire_time=expire_time
        )

        # Generate QR IMAGE with ENCRYPTED token inside
        qr = qrcode.make(encrypted_uuid)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_img_base64 = base64.b64encode(buffer.getvalue()).decode()

        return Response({
            "qr_uuid": encrypted_uuid,   # this is what student sends back
            "qr_image": f"data:image/png;base64,{qr_img_base64}",
            "expires_at": expire_time
        })


class MarkAttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "student":
            return Response({"error": "Only students allowed"}, status=403)

        # 1️⃣ Get encrypted UUID
        encrypted_uuid = request.data.get("qr_uuid")
        if not encrypted_uuid:
            return Response({"error": "qr_uuid is required"}, status=400)

        # 2️⃣ Decrypt
        try:
            real_uuid = decrypt_token(encrypted_uuid)
        except Exception:
            return Response({"error": "Invalid QR Token"}, status=400)

        # 3️⃣ Fetch QR object
        try:
            qr_obj = AttendanceQRCode.objects.get(uuid=real_uuid)
        except AttendanceQRCode.DoesNotExist:
            return Response({"error": "Invalid QR Code"}, status=400)

        # 4️⃣ Check expiry
        if qr_obj.expire_time < timezone.now():
            return Response({"error": "QR expired"}, status=400)

        # 5️⃣ GEO-FENCING CHECKS (Apply Steps 3,4,5,6 here)
        if not DEV_MODE:

            # Step 3️⃣ Receive lat/lng/accuracy/mock values
            try:
                lat = float(request.data.get("lat"))
                lng = float(request.data.get("lng"))
                accuracy = float(request.data.get("accuracy"))
            except:
                return Response({"error": "Invalid GPS data"}, status=400)

            mock = request.data.get("mock", False)

            # Step 4️⃣ Reject mock GPS
            if mock is True:
                return Response({"error": "Mock Location detected"}, status=400)

            # Step 5️⃣ Minimum GPS accuracy requirement
            if accuracy > 50:    # require < 50 meter accuracy
                return Response({"error": "Weak GPS signal. Move outdoors."}, status=400)

            # Step 6️⃣ Calculate distance from college
            distance = distance_m(lat, lng, COLLEGE_LAT, COLLEGE_LNG)

            if distance > GEOFENCE_RADIUS_METERS:
                return Response(
                    {"error": "Outside campus boundary. Attendance blocked."},
                    status=400
                )

        else:
            # DEV MODE QUICK VALUES
            lat = None
            lng = None
            accuracy = None
            distance = 0

        # 7️⃣ Save attendance with geofence logs
        Attendance.objects.update_or_create(
            student=request.user,
            class_session=qr_obj.class_session,
            date=timezone.now().date(),
            defaults={
                "present": True,
                "lat": lat,
                "lng": lng,
                "distance_from_college": distance,
                "gps_accuracy": accuracy,
                "is_mock_location": mock,
            },
        )

        return Response({"success": True, "message": "Attendance marked"})



class ViewAttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request): 
        if request.user.role not in ["teacher", "admin"]:
            return Response({"error": "Only teachers allowed"}, status=403)

        year = request.query_params.get("year")
        semester = request.query_params.get("semester")
        subject = request.query_params.get("subject")
        section = request.query_params.get("section")
        date_str = request.query_params.get("date")

        # Validate date
        try:
            from datetime import datetime
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            return Response({"error": "Invalid date format (YYYY-MM-DD)"}, status=400)

        sessions = ClassSession.objects.filter(teacher=request.user)

        if year:
            sessions = sessions.filter(year=year)
        if semester:
            sessions = sessions.filter(semester=semester)
        if subject:
            sessions = sessions.filter(subject__icontains=subject)
        if section:
            sessions = sessions.filter(section__icontains=section)

        if not sessions.exists():
            return Response({"error": "No matching class sessions"}, status=404)

        attendance = Attendance.objects.filter(
            class_session__in=sessions,
            date=date
        ).select_related("student", "class_session")

        output = []
        for r in attendance:
            output.append({
                "student_id": r.student.id,
                "student_name": r.student.get_full_name(),
                "present": r.present,
                "subject": r.class_session.subject,
                "year": r.class_session.year,
                "semester": r.class_session.semester,
                "section": r.class_session.section,
            })

        return Response(output)


class StudentHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "student":
            return Response({"error": "Only students allowed"}, status=403)

        attendance = Attendance.objects.filter(student=request.user)
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)
