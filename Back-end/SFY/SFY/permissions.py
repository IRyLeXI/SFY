import datetime
from rest_framework import permissions
from django.utils import timezone

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner.id == request.user.id or request.user.is_staff
    
    
class IsAuthorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_author or request.user.is_staff
    
    
class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print('qqq')
        return obj.id == request.user.id or request.user.is_staff
    
    
class IsSongOwnerOrAdmin(permissions.BasePermission):
     def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.authors.filter(id=request.user.id).exists()
    
    
class IsAlbumPublishedOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.publish_date<=timezone.now()
    

class IsPlaylistPrivateOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_private:
            return request.user.id == obj.owner.id or request.user.is_staff
        
        return True