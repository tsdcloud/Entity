from rest_framework.permissions import BasePermission


class IsAddService(BasePermission):
    """ add service """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'add_service' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsViewAllService(BasePermission):
    """ view all service """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'view_service_all' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsViewDetailService(BasePermission):
    """ view detail service """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'view_service_detail' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsChangeService(BasePermission):
    """ update service """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'change_service' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsDestroyService(BasePermission):
    """ destroy service """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'delete_service' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsRestoreService(BasePermission):
    """ restore service """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'active_service' in user['user']['user_permissions']:
                return True
            else:
                return False
