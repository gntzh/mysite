from blog.models import Post, Tag, Category
from django.core.exceptions import ValidationError
import pytest


class TestCategoryParent:
    def test_own(self, cate):
        cate.parent = cate
        with pytest.raises(ValidationError):
            cate.clean()

    def test_others(self, cate, admin_user):
        cate.parent = Category.objects.create(
            name='test_self', owner=admin_user)
        with pytest.raises(ValidationError):
            cate.clean()
