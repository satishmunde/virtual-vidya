from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core import serializers
from .models import Classroom, Note, Assignment, Submission
from .serializers import ClassroomSerializer, NoteSerializer, AssignmentSerializer, SubmissionSerializer
from core.models import User
from django.db.models import Q

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'teacher'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'student'



    
class ClassroomListCreateView(generics.ListCreateAPIView):
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'teacher':
            return Classroom.objects.filter(teacher=user)
        return Classroom.objects.filter(students=user)

    def perform_create(self, serializer):
        if self.request.user.user_type != 'teacher':
            raise serializers.ValidationError("Only teachers can create classrooms.")
        serializer.save(teacher=self.request.user)

class ClassroomJoinView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        code = request.data.get('code')
        try:
            classroom = Classroom.objects.get(code=code)
            if request.user in classroom.students.all():
                return Response({"detail": "Already enrolled."}, status=status.HTTP_400_BAD_REQUEST)
            classroom.students.add(request.user)
            return Response(ClassroomSerializer(classroom).data)
        except Classroom.DoesNotExist:
            return Response({"detail": "Invalid classroom code."}, status=status.HTTP_404_NOT_FOUND)



class ClassroomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Classroom.objects.filter(Q(teacher=user) | Q(students=user))

class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        classroom_id = self.request.query_params.get('classroom_id')
        if classroom_id:
            return Note.objects.filter(classroom_id=classroom_id, is_public=True) | Note.objects.filter(classroom_id=classroom_id, user=user)
        return Note.objects.filter(user=user)

    def perform_create(self, serializer):
        classroom = serializer.validated_data['classroom']
        if self.request.user not in classroom.students.all() and self.request.user != classroom.teacher:
            raise serializers.ValidationError("You are not part of this classroom.")
        serializer.save(user=self.request.user)

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(Q(user=user) | Q(is_public=True))

class AssignmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        classroom_id = self.request.query_params.get('classroom_id')
        if classroom_id:
            classroom = Classroom.objects.get(id=classroom_id)
            if user == classroom.teacher:
                return Assignment.objects.filter(classroom_id=classroom_id)
            return Assignment.objects.filter(classroom_id=classroom_id, classroom__students=user)
        return Assignment.objects.filter(classroom__teacher=user)

    def perform_create(self, serializer):
        classroom = serializer.validated_data['classroom']
        if self.request.user != classroom.teacher:
            raise serializers.ValidationError("Only teachers can create assignments.")
        serializer.save()

class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Assignment.objects.filter(Q(classroom__teacher=user) | Q(classroom__students=user))

class SubmissionListCreateView(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        assignment_id = self.request.query_params.get('assignment_id')
        if assignment_id:
            assignment = Assignment.objects.get(id=assignment_id)
            if user == assignment.classroom.teacher:
                return Submission.objects.filter(assignment_id=assignment_id)
            return Submission.objects.filter(assignment_id=assignment_id, student=user)
        return Submission.objects.filter(student=user)

    def perform_create(self, serializer):
        assignment = serializer.validated_data['assignment']
        if self.request.user not in assignment.classroom.students.all():
            raise serializers.ValidationError("You are not enrolled in this classroom.")
        serializer.save(student=self.request.user)

class SubmissionDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Submission.objects.filter(Q(student=user) | Q(assignment__classroom__teacher=user))