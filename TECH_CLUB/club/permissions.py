from rest_framework import permissions
from .models import Club
from .models import Project, Submission


class IsClubMember(permissions.BasePermission):
    def has_permission(self, request, view):
        # For create views
        club_id = view.kwargs.get('club_id')
        if club_id:
            club = Club.objects.get(pk=club_id)
            return request.user in club.members.all() or request.user == club.created_by
        return True

    def has_object_permission(self, request, view, obj):
        # For object-level permissions
        if isinstance(obj, Club):
            return request.user in obj.members.all() or request.user == obj.created_by
        elif isinstance(obj, Project):
            return request.user in obj.club.members.all() or request.user == obj.club.created_by
        elif isinstance(obj, Submission):
            return request.user in obj.project.club.members.all() or request.user == obj.project.club.created_by
        return False