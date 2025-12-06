from django.urls import path
from .views import GenerateQRCodeAPIView, MarkAttendanceAPIView, StudentHistoryAPIView, ViewAttendanceAPIView

urlpatterns = [
    path("generate-qr/", GenerateQRCodeAPIView.as_view()),
    path("mark/", MarkAttendanceAPIView.as_view()),
    path("view/", ViewAttendanceAPIView.as_view()),
    path("history/", StudentHistoryAPIView.as_view()),
]
