from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
