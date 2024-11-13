from typing import List

from rest_framework.permissions import AllowAny
from rest_framework.urls import path

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import *

from company.models import *
from core.urls import urlpatterns


'''

Chain of responsibity Pattern

'''

class AbstractAPIRegistrationHandler:

    @classmethod
    def handle(cls):
        return GetAPIForRegistrationFromDB.next()
    
    @classmethod
    def register(cls, api: API):
        return CreateAPIEnpoint.next(api)



class GetAPIForRegistrationFromDB(AbstractAPIRegistrationHandler):

    @classmethod
    def _load_apis(cls):
        return API.objects.all()

    @classmethod
    def next(cls):
        return BuildAPIEnpointFlow.next(cls._load_apis())
    

class BuildAPIEnpointFlow(AbstractAPIRegistrationHandler):
    
    @classmethod
    def next(cls, apis: List[API]):
        for api in apis:
            CreateAPIEnpoint.next(api)


class CreateAPIEnpoint(AbstractAPIRegistrationHandler):

    @classmethod
    def build_flow(cls, api: API):
        return APIFlowBuilder(api)

    @classmethod
    def next(cls, api: API):
        '''
        TODO: handle path params in handler functions
        '''
        endpoint_prefix = api.project.company.route
        endpoint_path = api.endpoint
        name = api.name
        handler = cls.build_flow(api).handler_class
        route = f"{endpoint_prefix}/{endpoint_path}"
        urlpattern = path(route, handler, name=name)
        urlpatterns.append(urlpattern)
        
class APIFlowBuilder(AbstractAPIRegistrationHandler):


    def __init__(self, api : API):
        super().__init__()
        self.api = api

    def _authentication(self):
        '''
        TODO: for now all apis are not authenticated need to a 
        authentication method to be implemented for the apis
        '''
        return AllowAny

    @api_view(["GET"])
    @permission_classes([AllowAny])
    def _get(self, request, **kwargs):
        return self._build_api_body(self.api.flow, request, **kwargs)


    @api_view(["post"])
    @permission_classes([AllowAny])
    def _post(self, request, **kwargs):
        return self._build_api_body(self.api.flow, request, **kwargs)

    
    @api_view(["put"])
    @permission_classes([AllowAny])
    def _put(self, request, **kwargs):
        return self._build_api_body(self.api.flow, request, **kwargs)

    @api_view(["delete"])
    @permission_classes([AllowAny])
    def _delete(self, request, **kwargs):
        return self._build_api_body(self.api.flow, request, **kwargs)


    def _handle_api_method(self):
        handler_method_name = f"_{self.api.method.lower()}"
        handler_method = getattr(self, handler_method_name)
        return handler_method



    def _build_api_body(self, flow_id, request, **kwargs):
        return LoadAPIBodyFromNeo(flow_id).build(request, **kwargs)

    @property
    def handler_class(self):
        view = self._handle_api_method()
        return view


class LoadAPIBodyFromNeo(AbstractAPIRegistrationHandler):

    def __init__(self, flow_id: str):
        super().__init__()
        self.flow_id = flow_id


    def build(self, request, **kwargs):
        return Response(status=HTTP_204_NO_CONTENT)