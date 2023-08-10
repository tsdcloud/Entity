from rest_framework.permissions import BasePermission


class IsViewAllBranch(BasePermission):
    """ view all branch """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'view_all_branch' in user['user']['user_permissions']:
                return True
            else:
                return False
