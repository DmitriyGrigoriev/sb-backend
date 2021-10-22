from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from apps.users.models import User

class PaginationData(PageNumberPagination):
    # page_size = 5
    page_size_query_param = 'rows_per_page'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            # 'rows': self.page_size,
            'data': data
        })

# Todo: if this filter will not to be using in future - deleted!
class UserFilter(filters.FilterSet):
    first_name = filters.CharFilter(lookup_expr='exact')
    middle_name = filters.CharFilter(lookup_expr='exact')
    last_name = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = User
        fields = [
            User.USERNAME_FIELD,
            'first_name',
            'middle_name',
            'last_name',
        ]


# Todo: if this filter will not to be using in future - deleted!
class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass
