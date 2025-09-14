# tutors/views.py
from rest_framework import viewsets, permissions
from .models import Tutor,TutorCourse,TutorCertificate, TutorEducation, TutorExperience
from .serializers import (
    TutorSerializer,
    TutorCourseSerializer,
    TutorCertificateSerializer,
    TutorEducationSerializer,
    TutorExperienceSerializer,
)



class ReadOnlyOrAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow anyone to GET/HEAD/OPTIONS; require auth for POST/PUT/PATCH/DELETE
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated




class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.select_related("user").prefetch_related(
        "certificates", "educations", "experiences","courses"
    )
    serializer_class = TutorSerializer
    permission_classes = [ReadOnlyOrAuth]

class TutorCourseViewSet(viewsets.ModelViewSet):
    queryset = TutorCourse.objects.all()
    serializer_class = TutorCourseSerializer
    permission_classes = [ReadOnlyOrAuth]

class TutorCertificateViewSet(viewsets.ModelViewSet):
    queryset = TutorCertificate.objects.all()
    serializer_class = TutorCertificateSerializer
    permission_classes = [ReadOnlyOrAuth]

class TutorEducationViewSet(viewsets.ModelViewSet):
    queryset = TutorEducation.objects.all()
    serializer_class = TutorEducationSerializer
    permission_classes = [ReadOnlyOrAuth]

class TutorExperienceViewSet(viewsets.ModelViewSet):
    queryset = TutorExperience.objects.all()
    serializer_class = TutorExperienceSerializer
    permission_classes = [ReadOnlyOrAuth]
