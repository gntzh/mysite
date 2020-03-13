from django.utils.functional import cached_property

from whoosh.fields import TEXT, ID, KEYWORD, STORED
from utils.search.fields import Model, Field
from blog.models import Post


class PostModel(Model):
    text = Field(template_path='blog/post.txt')
    title = Field(whoosh_field=STORED)
    content = Field(whoosh_field=STORED)
    model = Post

    def get_all(self):
        return self.model.public.all()

    def get_need(self):
        return self.model.public.filter(need_index=True)
