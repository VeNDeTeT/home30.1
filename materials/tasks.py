from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_course_update_email(course_id):
    from materials.models import (
        Course,
        Subscription,
    )  # импорт внутри, чтобы избежать циклов

    course = Course.objects.get(id=course_id)
    subs = Subscription.objects.filter(course=course)

    for sub in subs:
        send_mail(
            subject=f"Обновление курса: {course.title}",
            message="Материалы курса были обновлены.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[sub.user.email],
            fail_silently=False,
        )
