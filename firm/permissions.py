from rest_framework.permissions import BasePermission

class IsAddFirm(BasePermission):
 
    def has_permission(self, request, view):
        if request.infoUser == None:
            return False
        else:
            user = request.infoUser
            if user['user'].get('is_superuser') == True:
                return True
            elif 'add_entity' in user['user']['user_permissions']:
                return True
            else:
                return False