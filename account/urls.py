from django.urls import path
from .views import ChangePasswordAPIView, LoginAPIView, AdminCreateUserAPIView, ProfileAPIView, UpdateProfileAPIView

urlpatterns = [
    path("login/", LoginAPIView.as_view()),
    path("admin/create-user/", AdminCreateUserAPIView.as_view()),
    path("profile/", ProfileAPIView.as_view()),
    path("profile/update/", UpdateProfileAPIView.as_view()),
    path("password/change/", ChangePasswordAPIView.as_view()),
]
