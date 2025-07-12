from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TutorViewSet

router = DefaultRouter()
router.register('tutors', TutorViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
