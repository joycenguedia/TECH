from django.urls import path, include

from .views import ClubListView, ClubCreateView, ClubDetailView, ClubJoinView, ProjectListView, ProjectCreateView, SubmissionListView, SubmissionCreateView


urlpatterns = [
    # Clubs
    path('clubs/', ClubListView.as_view(), name='club-list'),
    path('clubs/create/', ClubCreateView.as_view(), name='club-create'),
    path('clubs/<int:pk>/', ClubDetailView.as_view(), name='club-detail'),
    path('clubs/<str:code>/join/', ClubJoinView.as_view(), name='club-join'),

    # Projects
    path('clubs/<int:club_id>/projects/', ProjectListView.as_view(), name='project-list'),
    path('clubs/<int:club_id>/projects/create/', ProjectCreateView.as_view(), name='project-create'),

    # Submissions
    path('projects/<int:project_id>/submissions/', SubmissionListView.as_view(), name='submission-list'),
    path('projects/<int:project_id>/submit/', SubmissionCreateView.as_view(), name='submission-create'),
]
