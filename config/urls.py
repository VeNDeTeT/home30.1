from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),

    #  АВТОРИЗАЦИЯ (ОТКРЫТЫЕ!):
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/", include("materials.urls")),
    path("api/users/", include("users.urls", namespace="users")),
]
