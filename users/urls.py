from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("payments/", views.PaymentListView.as_view(), name="payments-list"),
    path("", views.UserListView.as_view(), name="user-list"),
    path("<int:pk>/", views.UserRetrieveUpdateDestroyView.as_view(), name="user-detail"),
]