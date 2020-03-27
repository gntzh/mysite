from rest_framework.pagination import CursorPagination, LimitOffsetPagination


class PostPagination(CursorPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class Pagination(CursorPagination):
    ordering = ['id']
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 30
