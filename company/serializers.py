from rest_framework.serializers import ModelSerializer
from .models import Company, Project, Environment, API, DBSecret
from core.serializers import ProjectLoggerSerializer
from core.router import AbstractAPIRegistrationHandler 


class CompanySerializer(ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ["route"]

    def create(self, validated_data):
        company: Company = super().create(validated_data)
        env = Environment(env="staging", company=company)
        env.save()
        env = Environment(env="prod", company=company)
        env.save()
        return company


class ProjectSerializer(ModelSerializer):
    # TODO: handle project secret_key visibility

    class Meta:
        model = Project
        exclude = ["secret_key"]
        read_only_fields = ["secret_key", "log_retention"]


    def to_representation(self, instance: Project):
        repr = super().to_representation(instance)
        repr["company"] = CompanySerializer(instance.company).data
        return repr


class EnvironmentSerializer(ModelSerializer):

    class Meta:
        model = Environment
        fields = "__all__"


class APISerializer(ModelSerializer):

    class Meta:
        model = API
        fields = "__all__"
        read_only_fields = ["flow"]

    def create(self, validated_data):
        instance : API = super().create(validated_data)
        AbstractAPIRegistrationHandler.register(instance)
        return instance


    def to_representation(self, instance : API):
        repr = super().to_representation(instance)
        repr["endpoint"] = f"/c/{instance.project.company.route}/{instance.endpoint}"
        return repr
    

class DBSecretsSerializer(ModelSerializer):

    class Meta:
        model = DBSecret
        fields = "__all__"