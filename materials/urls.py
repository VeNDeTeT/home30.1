from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from .views import CoursePaymentAPIView

app_name = "materials"

router = DefaultRouter()
router.register(r"courses", views.CourseViewSet)

urlpatterns = [
    *router.urls,
    path("lessons/", views.LessonListCreateView.as_view(), name="lesson-list-create"),
    path(
        "lessons/<int:pk>/",
        views.LessonRetrieveUpdateDestroyView.as_view(),
        name="lesson-detail",
    ),
    path(
        "courses/<int:course_id>/subscribe/",
        views.CourseSubscribeAPIView.as_view(),
        name="course-subscribe",
    ),
    path("payments/create/", CoursePaymentAPIView.as_view(), name="course-payment"),
]