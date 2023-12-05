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


class IsAddSite(BasePermission):
    """ add un site """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'add_site' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewAllSite(BasePermission):
    """ see all site """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_all_site' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsViewDetailSite(BasePermission):
    """ see detail site """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'view_detail_site' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsChangeSite(BasePermission):
    """ change site """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'change_site' in user['member']['user_permissions']:
                return True
            else:
                return False


class IsDeleteSite(BasePermission):
    """ delete site """

    def has_permission(self, request, view):
        if request.infoUser is None:
            return False
        else:
            user = request.infoUser
            if user['member'].get('is_superuser') is True:
                return True
            elif 'delete_site' in user['member']['user_permissions']:
                return True
            else:
                return False
