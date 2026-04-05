from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views
from users.views import UserRegisterView

schema_view = get_schema_view(
    openapi.Info(
        title="API Курсов с оплатой Stripe",
        default_version="v1",
        description="Документация API: курсы, уроки, подписки, пользователи",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),

    # auth
    path("api/auth/register/", UserRegisterView.as_view(), name="register"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # api
    path("api/", include("materials.urls")),
    path("api/users/", include(("users.urls", "users"), namespace="users")),

    # docs
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]