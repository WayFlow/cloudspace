from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from utils.errors import build_error_message
from .serializers import CompanySerializer
from rest_framework.response import Response
from rest_framework.status import *

from utils.constants import ResponseDataKey


class CompanyListAPIView(ListAPIView): ...


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
                    {
                        ResponseDataKey.DATA_KEY: serializer.data,
                        ResponseDataKey.MESSAGE_KEY: "Successfully created!",
                    },
                    status=HTTP_201_CREATED,
                )
            return Response(
                {ResponseDataKey.ERROR_KEY: build_error_message(serializer.errors)},
                status=HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(e)
            return Response(
                {ResponseDataKey.ERROR_KEY: str(e)}, status=HTTP_400_BAD_REQUEST
            )
