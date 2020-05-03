from datetime import timedelta
from celery.schedules import crontab
from django.conf import settings

from mysite.celery import app
from blog.search import PostModel
from libs.search.backend import SearchBackend


@app.task
def index_posts():
    post_model = PostModel()
    qs = post_model.get_need()
    backend = SearchBackend(
        post_model, settings.INDEX_DIR, post_model.indexname)
    backend.build_index(qs)
    qs.update(need_index=False)
