from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import User, Payment
from .serializers import (
    UserProfileSerializer,
    PaymentSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные

    def get_object(self):
        return self.request.user  # Текущий пользователь


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_date"]
    permission_classes = [IsAuthenticated]


class UserRegisterView(generics.CreateAPIView):
    """Регистрация (ОТКРЫТАЯ!)"""

    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]  # ← ДЛЯ ВСЕХ!


class UserListCreateView(generics.ListCreateAPIView):
    """Список + Создание пользователей (только авторизованные)"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Детали/Обновление/Удаление пользователя (только авторизованные)"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
