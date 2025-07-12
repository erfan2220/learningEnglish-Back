from rest_framework import serializers
from .models import Course, Tutor, Student, Lesson, Homework, Review

# Serializer for Tutor
class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['user', 'profile_picture', 'languages_spoken']

# Serializer for Course
class CourseSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer()
    lessons = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all(), many=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price_per_hour', 'language', 'level', 'schedule_day', 'schedule_start', 'schedule_end', 'capacity']

# Serializer for Student
class StudentSerializer(serializers.ModelSerializer):
    courses_list = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True)
    favorite_tutors = serializers.PrimaryKeyRelatedField(queryset=Tutor.objects.all(), many=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'courses_list', 'favorite_tutors', 'student_active', 'student_homework_completed']

# Serializer for Lesson
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'lesson_video', 'lesson_document']

# Serializer for Homework
class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['id', 'title', 'document', 'due_date']

# Serializer for Review
class ReviewSerializer(serializers.ModelSerializer):
    class ReviewSerializer(serializers.ModelSerializer):
        student = StudentSerializer()
        tutor = TutorSerializer()

    class Meta:
        model = Review
        fields = ['student', 'tutor', 'review_text', 'rating', 'review_date']
