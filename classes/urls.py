from django.urls import path
from .views import ClassSessionListAPIView, AssignUsersToClassAPIView, StudentRoutineAPIView, TeacherRoutineAPIView

urlpatterns = [
    path("list/", ClassSessionListAPIView.as_view()),
    path("assign/", AssignUsersToClassAPIView.as_view()),
    path("routine/teacher/", TeacherRoutineAPIView.as_view()),
    path("routine/student/", StudentRoutineAPIView.as_view()),
]
