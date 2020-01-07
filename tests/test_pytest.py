import pytest
from blog.models import Category


@pytest.mark.skip('测试pytest')
def test_one():
    x = 'this'
    assert 'h' in x
    assert 'j' in x


@pytest.mark.django_db
@pytest.mark.xfail
def test_db():
    qs = Category.objects.filter(id=-1)
    assert qs.exists()


# def test_request_factory(rf):
#     res =
#     assert 0
