from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path

from orders.views import DevicesServiceAPIView, PlaceAPIView, SnacksServiceAPIView, OrderCreateAPIView, \
    OrderSnacksAPIView, OrderDetailAPIView, OrderDetailUpdateAPIView
from users.views import UserViewSet, ResetPasswordView, LoginAPIView
from users.views import RegisterAPIView, LogoutView, PasswordChangeView
from rest_framework_simplejwt.views import TokenRefreshView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("order-create", OrderCreateAPIView)
router.register("orders", OrderDetailAPIView)
router.register("order-detail-update", OrderDetailUpdateAPIView)
router.register("create-update-device", DevicesServiceAPIView)
router.register("create-update-place", PlaceAPIView)
router.register("create-update-snack", SnacksServiceAPIView)
router.register("create-update-delete-ordersnacks", OrderSnacksAPIView)

app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path('register/', RegisterAPIView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
