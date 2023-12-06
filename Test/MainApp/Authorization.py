from rest_framework import authentication, exceptions
import datetime
from .models import CustomUser
import jwt

from Test import settings


class JWTAuthorization(authentication.BaseAuthentication):
    key = 'Token'

    def authenticate(self, request):
        request.user = None
        auth = authentication.get_authorization_header(request).split()
        if not auth or self.key.lower().encode() != auth[0].lower() or len(auth) != 2:
            return None
        token = auth[1].decode('utf-8')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = CustomUser.objects.get(pk=payload.get('id'))
        except Exception as e:
            print(f"Error: {e}")
            msg = "Failed auth"
            raise exceptions.AuthenticationFailed(msg)
        if payload['exp'] < datetime.datetime.now().timestamp():
            raise exceptions.NotAuthenticated()
        return (user, token)
