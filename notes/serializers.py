from rest_framework import serializers
from .models import Classroom, Note, Assignment, Submission
from core.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

class ClassroomSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    students = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'code', 'teacher', 'students','created_at', 'description']
        read_only_fields = ['code', 'teacher', 'created_at']

class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())

    class Meta:
        model = Note
        fields = ['id', 'classroom', 'user', 'title', 'content', 'file' ,'is_public', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class AssignmentSerializer(serializers.ModelSerializer):
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())

    class Meta:
        model = Assignment
        fields = ['id', 'classroom', 'title', 'description', 'due_date', 'max_points', 'created_at']
        read_only_fields = ['created_at']

class SubmissionSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    assignment = serializers.PrimaryKeyRelatedField(queryset=Assignment.objects.all())

    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'student', 'content', 'submitted_at', 'grade', 'feedback']
        read_only_fields = ['student', 'submitted_at']