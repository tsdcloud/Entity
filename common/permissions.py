from rest_framework.permissions import BasePermission
 
class IsAuthenticated(BasePermission):
    """ check is user is authenticated """
    def has_permission(self, request, view):
        return True if request.infoUser is not None else False

class IsDeactivate(BasePermission):
    """ suspend a url """
    def has_permission(self, request, view):
        return False