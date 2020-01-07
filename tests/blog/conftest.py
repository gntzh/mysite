import pytest
from blog.models import Post, Category, Tag


@pytest.fixture
def cate(db, user):
    return Category.objects.create(name='test_1_l1', parent=None, owner=user)
