from rest_framework import permissions
from .models import Club, Project, Submission

class IsClubMember(permissions.BasePermission):
    def has_permission(self, request, view):
        club_id = view.kwargs.get('club_id')
        if club_id:
            try:
                club = Club.objects.get(pk=club_id)
                return request.user in club.members.all() or request.user == club.created_by
            except Club.DoesNotExist:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'club'):  # For Project/Submission
            club = obj.club
        elif hasattr(obj, 'members'):  # For Club
            club = obj
        else:
            return False
            
        return request.user in club.members.all() or request.user == club.created_by

class IsClubCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'club'):  # For Project/Submission
            return request.user == obj.club.created_by
        elif hasattr(obj, 'created_by'):  # For Club
            return request.user == obj.created_by
        return False
    
    

# from rest_framework import permissions
# from .models import Club, Project, Submission



# class IsInstructor(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return hasattr(request.user, 'role') and request.user.role == 'instructor'

# class IsClubMember(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # For create views
#         club_id = view.kwargs.get('club_id')
#         if club_id:
#             club = Club.objects.get(pk=club_id)
#             return request.user in club.members.all() or request.user == club.created_by
#         return True

#     def has_object_permission(self, request, view, obj):
#         # For object-level permissions
#         if isinstance(obj, Club):
#             return request.user in obj.members.all() or request.user == obj.created_by
#         elif isinstance(obj, Project):
#             return request.user in obj.club.members.all() or request.user == obj.club.created_by
#         elif isinstance(obj, Submission):
#             return request.user in obj.project.club.members.all() or request.user == obj.project.club.created_by
#         return False
    

#     class IsClubCreator(permissions.BasePermission):
#      def has_object_permission(self, request, view, obj):
#         if isinstance(obj, Club):
#             return request.user == obj.created_by
#         elif isinstance(obj, Project):
#             return request.user == obj.club.created_by
#         elif isinstance(obj, Submission):
#             return request.user == obj.project.club.created_by
#         return False