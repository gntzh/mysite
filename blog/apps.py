from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = '博客'

    def ready(self):
        from . import signals
