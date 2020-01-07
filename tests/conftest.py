import pytest
from time import time as now


@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create_user(username='test'+str(now()), email='testmail@test.com')


@pytest.fixture()
def api_rf():
    """RequestFactory instance"""
    try:
        from rest_framework.test import APIRequestFactory
    except ImportError:
        pytest.skip('缺失Django REST Framework')
    return APIRequestFactory()
