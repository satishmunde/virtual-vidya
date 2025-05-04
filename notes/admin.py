from django.contrib import admin
from .models import Classroom, Note, Assignment, Submission

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'code', 'teacher__email')
    readonly_fields = ('code',)
    filter_horizontal = ('students',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'classroom', 'user', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at', 'classroom')
    search_fields = ('title', 'content', 'user__email')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'classroom', 'due_date', 'max_points', 'created_at')
    list_filter = ('due_date', 'created_at', 'classroom')
    search_fields = ('title', 'description')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'grade')
    list_filter = ('submitted_at', 'assignment')
    search_fields = ('student__email', 'assignment__title')