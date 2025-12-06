from django.urls import path
from .views import ClassSessionListAPIView, AssignUsersToClassAPIView

urlpatterns = [
    path("list/", ClassSessionListAPIView.as_view()),
    path("assign/", AssignUsersToClassAPIView.as_view()),
]
