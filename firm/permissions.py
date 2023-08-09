from rest_framework.permissions import BasePermission


class IsAddFirm(BasePermission):
    """ add entity """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'add_entity' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsViewAllFirm(BasePermission):
    """ view all entity """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'view_entity_all' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsViewDetailFirm(BasePermission):
    """ view detail entity """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'view_entity_detail' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsChangeFirm(BasePermission):
    """ update entity """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'change_entity' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsDestroyFirm(BasePermission):
    """ update entity """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'delete_entity' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsRestoreFirm(BasePermission):
    """ restore entity """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'active_entity' in user['user']['user_permissions']:
                return True
            else:
                return False
