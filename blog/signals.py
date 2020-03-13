from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post


@receiver(m2m_changed, sender=Post.likes.through)
def post_like_changed(sender, instance, action, **kwargs):
    if action.startswith('post'):
        # 潜在bug, 必须保证由Post发起多对多字段的操作
        print(instance)
        instance.like_count = instance.likes.count()
        instance.save()
