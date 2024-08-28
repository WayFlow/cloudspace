from django.contrib.auth import get_user_model
from rest_framework import serializers

Account = get_user_model()


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ("id", "email", "password", "details", "username", "first_name", "last_name")

    def create(self, validated_data):
        account = Account.objects.create_user(
            email=validated_data.pop("email", None),
            password=validated_data.pop("password", None),
            **validated_data
        )
        return account
