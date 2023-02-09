from django.urls import path

from .views import OrdersAPIView, OrderDetailAPIView, OrderCreateAPIView, DevicesAPIView, SnacksAPIView, PlacesAPIView

app_name = "orders"
urlpatterns = [
    path("", OrdersAPIView.as_view(), name="orders"),
    # path("create/", OrderCreateAPIView.as_view()),
    path("details/", OrderDetailAPIView.as_view()),
    path("get-devices/", DevicesAPIView.as_view()),
    path("get-snacks/", SnacksAPIView.as_view()),
    path("get-places/", PlacesAPIView.as_view()),

]
