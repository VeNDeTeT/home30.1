from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)

urlpatterns = [
    *router.urls,
    path('lessons/', views.LessonListCreateView.as_view()),
    path('lessons/<int:pk>/', views.LessonRetrieveUpdateDestroyView.as_view()),
]
