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


class IsViewDetailBranch(BasePermission):
    """ view detail branch """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'view_detail_branch' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsAddBranch(BasePermission):
    """ view detail branch """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'add_branch' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsChangeBranch(BasePermission):
    """ update branch """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'change_branch' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsDestroyBranch(BasePermission):
    """ destroy branch """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'delete_branch' in user['user']['user_permissions']:
                return True
            else:
                return False


class IsRestoreBranch(BasePermission):
    """ restore branch """
    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') is True:
                return True
            elif 'restore_branch' in user['user']['user_permissions']:
                return True
            else:
                return False
