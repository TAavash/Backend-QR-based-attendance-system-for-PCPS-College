from django.urls import path
from .views import ClassSessionListAPIView

urlpatterns = [
    path("list/", ClassSessionListAPIView.as_view()),
]
