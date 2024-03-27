from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSerPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        next_link = ""
        previous_link = ""

        if self.get_next_link() is not None:
            next_link = self.get_next_link()
        if self.get_previous_link() is not None:
            previous_link = self.get_previous_link()

        return Response({
            'links': {
                'next': next_link,
                'previous': previous_link,
            },
            'count': self.page.paginator.count,
            'results': data
        })


class MeetingsPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'

    max_page_size = 1000

    def get_paginated_response(self, data):
        next_link = ""
        previous_link = ""

        if self.get_next_link() is not None:
            next_link = self.get_next_link()
        if self.get_previous_link() is not None:
            previous_link = self.get_previous_link()

        return Response({
            'links': {
                'next': next_link,
                'previous': previous_link,
            },
            'meta': {
                'page_count': self.page.paginator.count // 15 + 1,
                'count': self.page.paginator.count,
            },
            'results': data
        })


class MeetingProfilesPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):

        next_link = ""
        previous_link = ""

        if self.get_next_link() is not None:
            next_link = self.get_next_link()
        if self.get_previous_link() is not None:
            previous_link = self.get_previous_link()

        return Response({
            'links': {
                'next': next_link,
                'previous': previous_link,
            },
            'meta': {
                'page_count': self.page.paginator.count // 15 + 1,
                'count': self.page.paginator.count,
            },
            'results': data
        })

