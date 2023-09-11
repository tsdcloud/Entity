from rest_framework.permissions import BasePermission


class IsAddLocation(BasePermission):
    """ add Location """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_location' in user['member']['user_permissions']:
                return True
            else:
                return False
