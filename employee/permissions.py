from rest_framework.permissions import BasePermission


class IsAddEmployee(BasePermission):
    """ add Employee """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'add_employee' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsViewAllEmployee(BasePermission):
    """ view all Employee """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'view_employee_all' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsViewDetailEmployee(BasePermission):
    """ view detail Employee """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'view_employee_detail' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsChangeEmployee(BasePermission):
    """ update Employee """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'change_employee' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsDestroyEmployee(BasePermission):
    """ destroy Employee """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'delete_employee' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsRestoreEmployee(BasePermission):
    """ restore Employee """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'active_employee' in user['user']['user_permissions']:
                return True
            else:
                return False
