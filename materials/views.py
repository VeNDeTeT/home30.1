from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Course, Lesson, CourseSubscription
from .serializers import CourseSerializer, LessonSerializer
from .services import create_payment
from .permissions import IsOwner


class CoursePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class LessonPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id"]
    pagination_class = CoursePagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            permission_classes = [IsOwner]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["course"]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LessonPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            permission_classes = [IsOwner]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class CourseSubscribeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        subscription, created = CourseSubscription.objects.get_or_create(
            user=request.user,
            course=course,
        )
        if created:
            message = "Подписка добавлена"
        else:
            subscription.delete()
            message = "Подписка удалена"

        return Response({"message": message})


class CoursePaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Оплата курса Stripe",
        operation_description="Создает платеж и Stripe checkout сессию",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "course_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID курса для оплаты",
                    example=2,
                )
            },
            required=["course_id"],
        ),
        responses={
            201: openapi.Response(
                "Платеж создан",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "payment_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "checkout_url": openapi.Schema(type=openapi.TYPE_STRING),
                        "session_id": openapi.Schema(type=openapi.TYPE_STRING),
                        "amount": openapi.Schema(type=openapi.TYPE_NUMBER),
                    },
                ),
            ),
            400: "Неверный course_id",
            404: "Курс не найден",
        },
    )
    def post(self, request):
        course_id = request.data.get("course_id")

        if not course_id:
            return Response(
                {"detail": "course_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment_data = create_payment(course_id, request.user)
        return Response(payment_data, status=status.HTTP_201_CREATED)