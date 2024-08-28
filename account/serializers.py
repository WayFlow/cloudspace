from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token

Account = get_user_model()


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ("id", "email", "password", "details")

    def create(self, validated_data):
        account = Account.objects.create_user(
            email=validated_data.pop("email", None),
            password=validated_data.pop("password", None),
            **validated_data
        )
        return account
