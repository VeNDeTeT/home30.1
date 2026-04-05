import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import Payment, Course

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment(course_id: int, user):
    """Создает платеж Stripe и запись в БД."""
    course = get_object_or_404(Course, id=course_id)

    product = stripe.Product.create(
        name=course.title,
        description=course.description or "",
    )

    price = stripe.Price.create(
        product=product.id,
        unit_amount=int(course.price * 100),
        currency="rub",
    )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
        success_url="http://localhost:8000/",
        cancel_url="http://localhost:8000/",
        metadata={
            "user_id": str(user.id),
            "course_id": str(course_id),
        },
    )

    payment = Payment.objects.create(
        course=course,
        user=user,
        stripe_session_id=session.id,
        stripe_checkout_url=session.url,
        amount=course.price,
        status="pending",
    )

    return {
        "payment_id": payment.id,
        "checkout_url": session.url,
        "session_id": session.id,
        "amount": float(course.price),
    }