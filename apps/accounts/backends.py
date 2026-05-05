from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class UsernameOrEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        login_value = username or kwargs.get(user_model.USERNAME_FIELD) or kwargs.get('email')
        if not login_value or not password:
            return None

        try:
            user = user_model.objects.get(
                Q(username__iexact=login_value) | Q(email__iexact=login_value)
            )
        except user_model.DoesNotExist:
            return None
        except user_model.MultipleObjectsReturned:
            user = user_model.objects.filter(
                Q(username__iexact=login_value) | Q(email__iexact=login_value)
            ).order_by('pk').first()

        if user is not None and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
