from django.contrib.auth import get_user_model
from django.contrib.syndication.views import Feed
from django.conf import settings
from .models import Post

User = get_user_model()


class PostFeed(Feed):

    def get_object(self, request, user_id):
        return User.objects.get(id=user_id)

    def title(self, user):
        return '%s的文章' % user.nickname or user.username

    def link(self, user):
        return '%s/user/%d' % (settings.FRONT_HOST, user.id)

    def description(self, user):
        return '%s的文章' % user.nickname or user.username

    def items(self, user):
        return Post.public.filter(author=user).order_by('-created')[:20]

    def item_title(self, post):
        return post.title

    def item_description(self, post):
        return post.content

    def item_link(self, post):
        return '%s/blog/%d' % (settings.FRONT_HOST, post.id)
