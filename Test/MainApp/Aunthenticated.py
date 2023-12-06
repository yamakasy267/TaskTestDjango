from rest_framework.permissions import IsAuthenticated

class Authenticated(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)