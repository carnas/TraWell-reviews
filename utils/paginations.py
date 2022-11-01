from rest_framework import pagination
from rest_framework.response import Response


class ReviewsPagination(pagination.PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'count': self.page.paginator.count,
            'results': data,
        })