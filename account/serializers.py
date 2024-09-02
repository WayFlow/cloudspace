from django.contrib.auth import get_user_model
from rest_framework import serializers
from company.serializers import CompanySerializer

Account = get_user_model()


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = (
            "id",
            "email",
            "password",
            "details",
            "username",
        )

    def create(self, validated_data):
        account = Account.objects.create_user(
            email=validated_data.pop("email", None),
            password=validated_data.pop("password", None),
            **validated_data
        )
        return account


class AccountDataSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = "__all__"


    def to_representation(self, instance):
        repr = super().to_representation(instance)
        companies = instance.get_user_companies.all()
        companies_data = CompanySerializer(companies, many=True).data
        repr['companies'] = companies_data
        return repr
