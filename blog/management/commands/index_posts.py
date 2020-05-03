import os.path

from django.conf import settings
from django.core.management.base import BaseCommand

from blog.search import PostModel
from libs.search.backend import SearchBackend


class Command(BaseCommand):
    help = "建立博客索引"

    def add_arguments(self, parser):
        parser.add_argument(
            '--rebuild', action='store_true',
            default=False,
            help='重建索引.'
        )

    def handle(self, *args, **options):
        post_model = PostModel()
        if options['rebuild']:
            qs = post_model.get_all()
            backend = SearchBackend(
                post_model, settings.INDEX_DIR, post_model.indexname, post_model._schema)
            self.stdout.write(self.style.SUCCESS('准备重建索引'))
            backend.build_index(qs)
            qs.update(need_index=False)
            self.stdout.write(self.style.SUCCESS(
                '索引重建成功, 共建立%d条' % qs.count()))
            return
        else:
            qs = post_model.get_need()
            self.stdout.write(self.style.SUCCESS('准备更新索引'))
            backend = SearchBackend(
                post_model, settings.INDEX_DIR, post_model.indexname)
            backend.build_index(qs)
            self.stdout.write(self.style.SUCCESS(
                '索引更新成功, 共更新/建立%d条' % qs.count()))
            qs.update(need_index=False)
