from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.views import APIView

from orders.models import Place, DevicesService, SnacksService, Quantity, Order
from orders.serializers import PlaceSerializer, DevicesServiceSerializer, \
    SnacksServiceSerializer, OrdersSerializer, OrderDetailSerializer, OrderCreateSerializer, \
    OrderQuantitySerializer

from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework import viewsets, status, permissions
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from users.permessions import AdminPermission
from users.utils import send_message

User = get_user_model()


class OrdersAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Order.objects.filter(is_deleted=False)
        return queryset

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
    http_method_names = ['get', 'put', 'patch']

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=request.query_params.get('order_id'))
        serializer = self.get_serializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=request.query_params.get('order_id'))
        stat = request.query_params.get('status')
        if stat == 'accepted':
            order.is_active = True
        elif stat == 'rejected':
            order.is_deleted = True
        order.save()
        # try:
        #     send_message({'to_email': request.user.email, 'body': "Post yaratildi"})
        # except:
        #     pass
        return Response(status=status.HTTP_200_OK)


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
        order = Order.objects.filter(id=int(serializer.data['id'])).first()
        if devices:
            for i in devices.split(","):
                device = DevicesService.objects.filter(id=int(i)).first()
                order.devices.add(device)
        # try:
        #     send_message({'to_email': request.user.email, 'body': "Post yaratildi"})
        # except:
        #     pass
        return Response({"id": serializer.data.get('id')}, status=status.HTTP_200_OK)


class OrderSnacksAPIView(viewsets.ModelViewSet):
    queryset = Quantity.objects.all()
    serializer_class = OrderQuantitySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["POST", "PUT", "DELETE"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = request.data
        snack_obj = []
        for i in data.get('snacks'):
            snack_obj.append(
                Quantity(order_id=data.get('order_id'), snack_id=int(i.get('snack')), number=int(i.get('number'))))
        Quantity.objects.bulk_create(snack_obj)
        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = request.data
        for i in data.get('snacks'):
            snack = Quantity.objects.filter(order_id=kwargs.get('pk'), snack_id=i.get('snack')).first()
            snack.number = int(i.get('number'))
            snack.save()
        return Response(status=status.HTTP_200_OK)


class PlacesAPIView(ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PlaceAPIView(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    http_method_names = ["POST", "PUT", "DELETE"]
    permission_classes = [IsAdminUser]


class SnacksAPIView(ListAPIView):
    queryset = SnacksService.objects.all()
    serializer_class = SnacksServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SnacksServiceAPIView(viewsets.ModelViewSet):
    queryset = SnacksService.objects.all()
    serializer_class = SnacksServiceSerializer
    http_method_names = ["POST", "PUT", "DELETE"]
    permission_classes = [IsAdminUser]


class DevicesAPIView(ListAPIView):
    queryset = DevicesService.objects.all()
    serializer_class = DevicesServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DevicesServiceAPIView(viewsets.ModelViewSet):
    queryset = DevicesService.objects.all()
    serializer_class = DevicesServiceSerializer
    http_method_names = ["POST", "PUT", "DELETE"]
    permission_classes = [IsAdminUser]
