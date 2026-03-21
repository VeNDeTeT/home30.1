from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("payments/", views.PaymentListView.as_view(), name="payments-list"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("", views.UserListCreateView.as_view(), name="user-list"),
    path(
        "<int:pk>/", views.UserRetrieveUpdateDestroyView.as_view(), name="user-detail"
    ),
]
