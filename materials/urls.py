from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from . import views
from .models import Course

app_name = "materials"

router = DefaultRouter()
router.register(r"courses", views.CourseViewSet)


urlpatterns = [
    *router.urls,

    path("lessons/", views.LessonListCreateView.as_view()),
    path("lessons/<int:pk>/", views.LessonRetrieveUpdateDestroyView.as_view()),
    path(
        "courses/<int:course_id>/subscribe/", views.CourseSubscribeAPIView.as_view()
    ),  # ← views. !
    path("lessons/", views.LessonListCreateView.as_view(), name="lesson-list-create"),
    path("lessons/<int:pk>/", views.LessonRetrieveUpdateDestroyView.as_view(), name="lesson-detail"),

]
