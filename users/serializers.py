from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Code

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "organization_name",
            "phone",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }

class UserOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "organization_name",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ['user', 'number']


class GetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
