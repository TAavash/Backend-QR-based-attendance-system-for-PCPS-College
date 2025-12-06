from django.urls import path
from .views import LoginAPIView, AdminCreateUserAPIView

urlpatterns = [
    path("login/", LoginAPIView.as_view()),
    path("admin/create-user/", AdminCreateUserAPIView.as_view()),

]
