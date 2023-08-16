from rest_framework.permissions import BasePermission


class IsAddFunction(BasePermission):
    """ add Function """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'add_function' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsViewAllFunction(BasePermission):
    """ view all Function """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'view_function_all' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsViewDetailFunction(BasePermission):
    """ view detail Function """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'view_function_detail' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsChangeFunction(BasePermission):
    """ update Function """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'change_function' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsDestroyFunction(BasePermission):
    """ destroy Function """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'delete_function' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsRestoreFunction(BasePermission):
    """ restore Function """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'active_function' in user['user']['user_permissions']:
                return True
            else:
                return False
