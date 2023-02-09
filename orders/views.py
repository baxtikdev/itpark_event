from pprint import pprint

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from orders.models import Place, DevicesService, SnacksService, Quantity, Order
from orders.serializers import PlaceSerializer, DevicesServiceSerializer, \
    SnacksServiceSerializer, OrdersSerializer, OrderDetailSerializer, QuantitySerializer, OrderCreateSerializer

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework import viewsets, status, permissions
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from users.utils import send_message

User = get_user_model()


class OrdersAPIView(ListAPIView):
    queryset = Order.objects.all().order_by('date')
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        orders = self.get_queryset()
        place_id = self.request.query_params.get('place_id')
        if place_id is not None:
            queryset = orders.filter(place_id=place_id)
        else:
            queryset = orders.filter(place=Place.objects.all().first())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderDetailAPIView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'put']


    def list(self, request, *args, **kwargs):
        orders = self.get_queryset().order_by('date')
        serializer = self.get_serializer(orders)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        order = self.get_queryset().filter(id=request.query_params.get('order_id')).first()
        serializer = self.get_serializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCreateAPIView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        devices = request.query_params.get('devices')
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if devices:
            order = Order.objects.filter(id=int(serializer.data['id'])).first()
            for i in devices.split(","):
                device = DevicesService.objects.filter(id=int(i)).first()
                order.devices.add(device)
        # try:
        #     send_message({'to_email': request.user.email, 'body': "Post yaratildi"})
        # except:
        #     pass
        return Response(status=status.HTTP_201_CREATED)


# PLACES
class PlacesAPIView(ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PlaceAPIView(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    http_method_names = ['post', 'put', 'delete']
    permission_classes = [IsAuthenticated]


# SNACKS
class SnacksAPIView(ListAPIView):
    queryset = SnacksService.objects.all()
    serializer_class = SnacksServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SnacksServiceAPIView(viewsets.ModelViewSet):
    queryset = SnacksService.objects.all()
    serializer_class = SnacksServiceSerializer
    http_method_names = ['post', 'put', 'delete']
    permission_classes = [IsAuthenticated]


# DEVICES
class DevicesAPIView(ListAPIView):
    queryset = DevicesService.objects.all()
    serializer_class = DevicesServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DevicesServiceAPIView(viewsets.ModelViewSet):
    queryset = DevicesService.objects.all()
    serializer_class = DevicesServiceSerializer
    http_method_names = ['post', 'put', 'delete']
    permission_classes = [IsAuthenticated]
