from rest_framework.pagination import CursorPagination


class PostPagination(CursorPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10


class Pagination(CursorPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100
