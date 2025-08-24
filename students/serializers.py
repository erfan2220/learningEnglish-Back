# students/serializers.py
from rest_framework import serializers

from courses.serializers import CourseSerializer
from tutors.serializers import TutorSerializer
from .models import Student  # Import your Student model

class StudentSerializer(serializers.ModelSerializer):
    courses_list = CourseSerializer(many=True, read_only=True)
    favourite_tutors = TutorSerializer(many=True, read_only=True)  # Corrected the field name to match model

    class Meta:
        model = Student
        fields = ['id', 'user', 'courses_list', 'favourite_tutors', 'student_active', 'student_homework_completed']
