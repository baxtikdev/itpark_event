from rest_framework import serializers
from .models import Order, Place, SnacksService, DevicesService, Quantity
from users.serializers import UserSerializer, UserOrderDetailSerializer


class SnacksServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnacksService
        fields = '__all__'


class QuantitySerializer(serializers.ModelSerializer):
    snack = SnacksServiceSerializer(read_only=True, many=False)

    class Meta:
        model = Quantity
        exclude = ['order']


class OrderBaseQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quantity
        exclude = ['order']


class OrderQuantitySerializer(serializers.Serializer):
    order_id = serializers.IntegerField(write_only=True, required=True)
    snacks = OrderBaseQuantitySerializer(write_only=True, many=True, required=True)


class DevicesServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevicesService
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('created_at', 'is_active', 'is_deleted')


class OrdersSerializer(serializers.ModelSerializer):
    user = UserOrderDetailSerializer(read_only=True, many=False)

    class Meta:
        model = Order
        fields = ['id', 'title', 'start', 'end', 'user', 'is_active']


class OrderUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'title', 'place', 'start', 'end', 'devices','people_number']


class OrderDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    devices = DevicesServiceSerializer(read_only=True, many=True)
    snacks = SnacksServiceSerializer(read_only=True, many=True)
    place = PlaceSerializer(read_only=True, many=False)

    class Meta:
        model = Order
        exclude = ('created_at', 'is_active', 'is_deleted')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['snacks'] = QuantitySerializer(instance.order_snack_quantity, many=True).data
        return response
