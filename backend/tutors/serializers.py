from rest_framework import serializers
from .models import Subject, TutorProfile,Availability, Lesson, Review
from django.contrib.auth.models import User


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields='__all__'


class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model=User
            fields=['id','username','first_name','last_name','email']


class TutorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    subjects = SubjectSerializer(many=True)

    class Meta:
        model=TutorProfile
        fields='__all__'

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model=Availability
        fields='__all__'
        read_only_fields=['tutor']


class LessonSerializer(serializers.ModelSerializer):
    tutor = TutorProfileSerializer(read_only=True)
    student = UserSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model=Lesson
        fields='__all__'
        read_only_fields=['tutor','student','status']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields='__all__'
        read_only_fields=['lesson']




