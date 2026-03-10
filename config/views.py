from django.shortcuts import render
from materials.models import Course, Lesson
from users.models import Payment


def home(request):
    """Главная страница"""
    context = {
        "courses_count": Course.objects.count(),
        "lessons_count": Lesson.objects.count(),
        "payments_count": Payment.objects.count(),
    }
    return render(request, "home.html", context)
