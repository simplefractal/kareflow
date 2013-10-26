from django.contrib.auth.models import User


def make_8_key():
    return User.objects.make_random_password(length=8)
