from django.db import models
from django.utils import timezone
import random
import string
from core.models import User

def generate_classroom_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Classroom(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=6, unique=True, default=generate_classroom_code)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classrooms_taught')
    students = models.ManyToManyField(User, related_name='classrooms_joined', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "Classroom"
        verbose_name_plural = "Classrooms"

class Note(models.Model):
    id = models.AutoField(primary_key=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='notes/files/', null=True, blank=True)  

    def __str__(self):
        return f"{self.title} in {self.classroom.name}"

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"

class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_points = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} in {self.classroom.name}"

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"

class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    content = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"Submission by {self.student} for {self.assignment.title}"

    class Meta:
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"