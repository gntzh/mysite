from django.contrib.auth import get_user_model

User = get_user_model()

user_id = 1


def createUser(username='test%d' % user_id, email='test%d@gmail.com' % user_id):
    User.objects.create_user(username=username, email=email)
    user_id += 1


def createAdmin(username='test%d' % user_id, email='test%d@gmail.com' % user_id):
    User.objects.create_superuser(username=username, email=email)
    user_id += 1
