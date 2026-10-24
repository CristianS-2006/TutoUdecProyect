from rest_framework.pagination import PageNumberPagination


class FlexiblePagination(PageNumberPagination):
    """Paginación estándar que permite pedir ?page_size=N (máximo 100)."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
