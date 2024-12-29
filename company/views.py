from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from django.db.models import Q

from utils.errors import build_error_message
from .serializers import (
    CompanySerializer,
    ProjectSerializer,
    EnvironmentSerializer,
    APISerializer,
    ProjectLoggerSerializer,
    DBSecretsSerializer
)
from rest_framework.response import Response
from rest_framework.status import *
from .models import Company, Project, API, Environment, ProjectLog, DBSecret
from .paginator import CustomCursorPagination

from utils.constants import ResponseDataKey

'''
TODO: for now I am fetching projects and env based on the 
created_by user use company_id to filter out the projects
env and DBSecrets
'''
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
        queryset = Project.objects.filter(company__created_by=self.request.user, company=self.kwargs.get('id'))
        return queryset

    def create(self, request, id, *args, **kwargs):
        try:
            print(id)
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

    def get(self, request, id,*args, **kwargs):
        queryset = Environment.objects.filter(company__created_by=request.user, company=id)
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


class ListProjectAPIsView(ListCreateAPIView):

    serializer_class = APISerializer

    def get_queryset(self):
        id = self.kwargs.get("id", None)
        queryset = API.objects.filter(project__id=id, project__company__created_by=self.request.user.id)
        return queryset
    


class ProjectLogsAPIView(ListAPIView):

    serializer_class = ProjectLoggerSerializer
    pagination_class = CustomCursorPagination

    '''
    TODO: implement filtering based on query start date and end date
    also implement text based search 
    docs: https://docs.djangoproject.com/en/5.1/ref/contrib/postgres/search/
    ''' 
    def get_queryset(self):
        env_id = self.request.query_params.get("envId")
        if env_id is None:
            return []
        # TODO: filter env logs from the query params later
        # start_from = self.request.query_params.get("from")
        # to = self.request.query_params.get("to")
        # search_params = self.request.query_params.get("q")
        # filters = Q()
        return ProjectLog.objects.filter(project=self.kwargs.get('id'), env=env_id, project__company__created_by=self.request.user)
    

class DBSecretView(ListCreateAPIView):
    serializer_class = DBSecretsSerializer


    def get_queryset(self):
        env_id = self.request.query_params.get("envId")
        project_id = self.kwargs.get('id')
        return DBSecret.objects.filter(project__company__created_by=self.request.user, env=env_id, project=project_id)