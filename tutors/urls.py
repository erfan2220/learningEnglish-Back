# tutors/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
     TutorViewSet,
    TutorCertificateViewSet,
    TutorEducationViewSet,
    TutorExperienceViewSet,
    TutorCourseViewSet,
)

router = DefaultRouter()
router.register("tutors", TutorViewSet, basename="tutors")
router.register(r'tutor-courses', TutorCourseViewSet)
# router.register("tutors", TutorViewSet, basename="tutors")
router.register("tutor-certificates", TutorCertificateViewSet, basename="tutor-certificates")
router.register("tutor-educations", TutorEducationViewSet, basename="tutor-educations")
router.register("tutor-experiences", TutorExperienceViewSet, basename="tutor-experiences")

urlpatterns = [
    path("api/", include(router.urls)),
]
