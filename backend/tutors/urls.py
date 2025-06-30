from django.urls import path
from . import views

urlpatterns = [
    path('subjects/', views.SubjectList.as_view(), name='subject-list'),
    path('tutors/', views.TutorList.as_view(), name='tutor-list'),
    path('tutors/<int:pk>/', views.TutorDetail.as_view(), name='tutor-detail'),
    path('tutors/<int:tutor_id>/availability/', views.AvailabilityList.as_view(), name='availability-list'),
    path('lessons/', views.LessonList.as_view(), name='lesson-list'),
    path('lessons/create/', views.LessonCreate.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', views.LessonDetail.as_view(), name='lesson-detail'),
    path('lessons/<int:lesson_id>/review/', views.ReviewCreate.as_view(), name='review-create'),
]