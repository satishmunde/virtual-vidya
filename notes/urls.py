from django.urls import path
from .views import (
    ClassroomListCreateView, ClassroomJoinView, ClassroomDetailView,
    NoteListCreateView, NoteDetailView,
    AssignmentListCreateView, AssignmentDetailView,
    SubmissionListCreateView, SubmissionDetailView
)

urlpatterns = [
    path('classrooms/', ClassroomListCreateView.as_view(), name='classroom-list-create'),
    path('classrooms/join/', ClassroomJoinView.as_view(), name='classroom-join'),
    path('classrooms/<int:pk>/', ClassroomDetailView.as_view(), name='classroom-detail'),
    path('notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('assignments/', AssignmentListCreateView.as_view(), name='assignment-list-create'),
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
    path('submissions/', SubmissionListCreateView.as_view(), name='submission-list-create'),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),
]