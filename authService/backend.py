from django.contrib.auth.backends import ModelBackend
from . import models
from django.db.models import Q

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = models.User.objects.get(Q(email=username))
            if user.check_password(password):
                return user
        except models.User.DoesNotExist:
            return None
        return None