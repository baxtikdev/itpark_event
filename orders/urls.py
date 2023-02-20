from django.urls import path

from .views import DevicesAPIView, SnacksAPIView, PlacesAPIView

app_name = "orders"
urlpatterns = [
    path("get-devices/", DevicesAPIView.as_view()),
    path("get-snacks/", SnacksAPIView.as_view()),
    path("get-places/", PlacesAPIView.as_view()),

]
