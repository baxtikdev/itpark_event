from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path

from orders.views import DevicesServiceAPIView, PlaceAPIView, SnacksServiceAPIView, OrderCreateAPIView
from users.views import UserViewSet, ResetPasswordView
from users.views import RegisterAPIView, LogoutView, PasswordChangeView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("order-create", OrderCreateAPIView)
router.register("create-update-device", DevicesServiceAPIView)
router.register("create-update-place", PlaceAPIView)
router.register("create-update-snack", SnacksServiceAPIView)

app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path('register/', RegisterAPIView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
