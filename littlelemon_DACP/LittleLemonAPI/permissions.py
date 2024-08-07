from rest_framework.permissions import BasePermission

class ManagerPermission(BasePermission):
    def has_permission(self, request, view):
        if(request.user.groups.filter(name='Manager').exists()):
            return True

        return False

class DeliveryPermission(BasePermission):
    def has_permission(self, request, view):
        if(request.user.groups.filter(name='Delivery crew').exists()):
            return True

        return False

class CustomerPermission(BasePermission):
    def has_permission(seld, request, view):
        if(not request.user.groups.all().exists()):
            return True

        return False
