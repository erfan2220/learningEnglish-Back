# students/serializers.py
from rest_framework import serializers

from courses.serializers import CourseSerializer
from tutors.serializers import TutorSerializer
from .models import Student  # Import your Student model

class StudentSerializer(serializers.ModelSerializer):
    courses_list =  CourseSerializer(many=True, read_only=True)
    favourite_tutors = TutorSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'courses_list', 'favorite_tutors', 'student_active', 'student_homework_completed']
