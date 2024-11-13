from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from utils.errors import build_error_message
from .serializers import (
    CompanySerializer,
    ProjectSerializer,
    EnvironmentSerializer,
    APISerializer
)
from rest_framework.response import Response
from rest_framework.status import *
from .models import Company, Project, API, Environment

from utils.constants import ResponseDataKey


class CompanyListAPIView(ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        queryset = Company.objects.filter(created_by=self.request.user)
        return queryset


class CreateCompanyView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            data: dict = request.data.copy()
            if "name" not in data:
                return Response(
                    {ResponseDataKey.ERROR_KEY: "name field is required"},
                    status=HTTP_400_BAD_REQUEST,
                )
            name: str = data.pop("name", "")
            name_array = name.split(" ")
            first_name = ""
            if len(name_array) > 1:
                first_name = name_array[0]
            last_name = ""
            for i in range(1, len(name_array)):
                last_name += name_array[i] + " "
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()
            data["created_by"] = request.user.id
            serializer = CompanySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=HTTP_201_CREATED,
                )
            return Response(
                {ResponseDataKey.ERROR_KEY: build_error_message(serializer.errors)},
                status=HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {ResponseDataKey.ERROR_KEY: str(e)}, status=HTTP_400_BAD_REQUEST
            )


class ProjectView(ListCreateAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(company__created_by=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = ProjectSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(
                {ResponseDataKey.ERROR_KEY: build_error_message(serializer.errors)},
                status=HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {ResponseDataKey.ERROR_KEY: str(e)}, status=HTTP_400_BAD_REQUEST
            )


class EnvironmentView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = Environment.objects.filter(company__created_by=request.user)
        serializer = EnvironmentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # try:
        #     data = request.data
        #     serializer = EnvironmentSerializer(data=data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=HTTP_201_CREATED)
        #     return Response(
        #         {ResponseDataKey.ERROR_KEY: build_error_message(serializer.errors)},
        #         status=HTTP_400_BAD_REQUEST,
        #     )
        # except Exception as e:
        #     return Response(
        #         {ResponseDataKey.ERROR_KEY: str(e)}, status=HTTP_400_BAD_REQUEST
        #     )
        return Response({"message": "Not allowed to create"}, status=HTTP_400_BAD_REQUEST)


class ListAPIProjectView(ListCreateAPIView):

    serializer_class = APISerializer

    def get_queryset(self):
        id = self.kwargs.get("id", None)
        queryset = API.objects.filter(project__id=id, project__company__created_by=self.request.user.id)
        return queryset
    
        