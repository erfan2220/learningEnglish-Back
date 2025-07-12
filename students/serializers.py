# students/serializers.py
from rest_framework import serializers
from .models import Student  # Import your Student model

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'courses_list', 'favorite_tutors', 'student_active', 'student_homework_completed']
