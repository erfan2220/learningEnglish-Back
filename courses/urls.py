from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, TutorViewSet, StudentViewSet, LessonViewSet, HomeworkViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register('tutors', TutorViewSet)
router.register('students', StudentViewSet)
router.register('lessons', LessonViewSet)
router.register('homeworks', HomeworkViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
