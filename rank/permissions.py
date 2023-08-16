from rest_framework.permissions import BasePermission


class IsAddRank(BasePermission):
    """ add Rank """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'add_rank' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsViewAllRank(BasePermission):
    """ view all Rank """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'view_rank_all' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsViewDetailRank(BasePermission):
    """ view detail Rank """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'view_rank_detail' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsChangeRank(BasePermission):
    """ update Rank """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'change_rank' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsDestroyRank(BasePermission):
    """ destroy Rank """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'delete_rank' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsRestoreRank(BasePermission):
    """ restore Rank """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'active_rank' in user['user']['user_permissions']:
                return True
            else:
                return False
