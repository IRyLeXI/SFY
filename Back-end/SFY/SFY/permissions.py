from rest_framework import permissions
from album.models import Album

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner.id == request.user.id or request.user.is_staff
    
    
class IsAuthorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_author or request.user.is_staff
    
    
class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id or request.user.is_staff
    
    
class IsSongOwnerOrAdmin(permissions.BasePermission):
     def has_object_permission(self, request, view, obj):
        # if request.user.is_staff:
        #     return True
        
        # if obj.authors.filter(id=request.user.id).exists():
        #     return True
        
        # return False
        return request.user.is_staff or obj.authors.filter(id=request.user.id).exists()