from django.shortcuts import render,get_object_or_404
from psutil import swap_memory
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from .models import Subject,TutorProfile,Availability,Lesson,Review
from .serializers import (
    SubjectSerializer,TutorProfileSerializer,
    AvailabilitySerializer,LessonSerializer,ReviewSerializer
)
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime,timedelta
from rest_framework.views import APIView

User = get_user_model()

# Create your views here.


class SubjectList(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]

class TutorList(generics.ListAPIView):
    serializer_class = TutorProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = TutorProfile.objects.filter(is_verified=True)

        subject = self.request.query_params.get('subject',None)

        if subject:
            queryset = queryset.filter(subject__id=subject)

            # Filter by min/max price if provided
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        if min_price:
            queryset = queryset.filter(hourly_rate__gte=min_price)
        if max_price:
            queryset = queryset.filter(hourly_rate__lte=max_price)

        return queryset


class TutorDetail(generics.RetrieveAPIView):
    queryset = TutorProfile.objects.all(is_verified=True)
    serializer_class = TutorProfileSerializer
    permission_classes = [permissions.AllowAny]

class AvailabilityList(generics.ListAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        tutor_id=self.kwargs['tutor_id']
        tutor = get_object_or_404(TutorProfile, id=tutor_id)
        return tutor.availabilities.all()

class LessonCreate(generics.CreateAPIView):
    serializer_class =  LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        tutor_id=self.request.kwargs['tutor_id']
        tutor = get_object_or_404(TutorProfile, id=tutor_id)


        start_time = datetime.fromisoformat(self.request.data['start_time'])
        end_time = datetime.fromisoformat(self.request.data['end_time'])


        overlapping_lessons =Lesson.objects.filter(
            tutor=tutor,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if overlapping_lessons:
            raise serializers.ValidationError("This time slot is already booked")

        serializer.save(
            tutor=tutor,
            student=self.request.user,
            status = 'pending'
        )


class LessonList(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'tutor':
            return Lesson.objects.filter(tutor__user=user)
        return Lesson.objects.filter(student=user)


class LessonDetail(generics.RetrieveUpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'tutor':
            return Lesson.objects.filter(tutor__user=user)
        return Lesson.objects.filter(student=user)

class ReviewList(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        lesson_id=self.kwargs['lesson_id']

        lesson = get_object_or_404(Lesson, id=lesson_id, student=self.request.user)

        if lesson.status != 'completed':
            raise serializers.ValidationError("This lesson is not completed")

        if hasattr(lesson, 'review'):
            raise serializers.ValidationError("This lesson is already reviewed")

        serializer.save(lesson=lesson)

