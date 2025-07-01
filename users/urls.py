from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.apps import UsersConfig
from users.views import PaymentViewSet, UserViewSet, UserCreatePIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path('register/', UserCreatePIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permissions=AllowAny), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
