from django.contrib.auth.backends import BaseBackend
from quizgame.models import CustomUser
from django.contrib.auth import get_user_model
class Auth(BaseBackend):
    def authenticate(request, username=None, password=None):
        try:
            user = CustomUser.objects.get(user_name=username)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None