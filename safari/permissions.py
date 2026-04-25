from rest_framework.permissions import BasePermission


class IsStaffUser(BasePermission):
    """Dashboard / admin API: authenticated staff (is_staff or linked StaffProfile)."""

    def has_permission(self, request, view):
        u = request.user
        if not u or not u.is_authenticated:
            return False
        if u.is_staff:
            return True
        return hasattr(u, "staff_profile")
