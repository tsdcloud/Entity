from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """ check is user is authenticated """
    def has_permission(self, request, view):
        return True if request.infoUser is not None else False


class IsSuperAdmin(BasePermission):
    """ check is user is super admin """
    def has_permission(self, request, view):
        return bool(request.infoUser and request.infoUser.get('is_superuser'))


class IsAddPermission(BasePermission):
    """ add permissions """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'add_permission' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsDeactivate(BasePermission):
    """ suspend a url """
    def has_permission(self, request, view):
        return False


class IsActivate(BasePermission):
    """ active a url """
    def has_permission(self, request, view):
        return True
