from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerTutorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # GET/HEAD/OPTIONS = آزاد
        if request.method in SAFE_METHODS:
            return True
        # باید لاگین باشد و صاحبش باشد
        return hasattr(request.user, "tutor") and obj.tutor == request.user.tutor
