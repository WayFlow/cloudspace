from rest_framework.pagination import CursorPagination
from cloudspace.settings import CURSOR_QUERY_PARAM_NAME, PAGINATION_PAGE_SIZE
from rest_framework.response import Response

'''
ordering = "-uploaded_on"
    page_size = PAGE_SIZE
    cursor_query_param = CURSOR_QUERY_PARAM_NAME

    def get_paginated_response(self, data):
        return Response(
            {
                "message": "Success",
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "data": data,
            }
        )
'''

class CustomCursorPagination(CursorPagination):

    ordering = "-created_at"
    page_size = PAGINATION_PAGE_SIZE
    cursor_query_param = CURSOR_QUERY_PARAM_NAME

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'data': data,
        })
    