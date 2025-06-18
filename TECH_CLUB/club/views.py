from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Club, Project, Submission
from .serializers import ClubSerializer, ProjectSerializer, SubmissionSerializer
from .permissions import IsClubMember, IsClubCreator

# Clubs
class ClubCreateView(generics.CreateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ClubJoinView(generics.UpdateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'code'

    def update(self, request, *args, **kwargs):
        club = self.get_object()
        if request.user in club.members.all():
            return Response(
                {'status': 'User is already a member'},
                status=status.HTTP_400_BAD_REQUEST
            )
        club.members.add(request.user)
        return Response({'status': 'Joined club successfully'}, status=status.HTTP_200_OK)

# Projects
class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsClubMember]

    def perform_create(self, serializer):
        club_id = self.kwargs.get('club_id')
        serializer.save(club_id=club_id, created_by=self.request.user)

# Submissions
class SubmissionCreateView(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsClubMember]

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        serializer.save(project_id=project_id, student=self.request.user)

class ClubListView(generics.ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClubDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticated, IsClubCreator]

class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsClubMember]

    def get_queryset(self):
        club_id = self.kwargs['club_id']
        return Project.objects.filter(club_id=club_id)

class SubmissionListView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsClubMember]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Submission.objects.filter(project_id=project_id)