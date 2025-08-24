from rest_framework import viewsets
from .models import Course, Tutor, Student, Lesson, Homework, Review
from .serializers import CourseSerializer, TutorSerializer, StudentSerializer, LessonSerializer, HomeworkSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Course
from .serializers import CourseSerializer
from .permissions import IsOwnerTutorOrReadOnly


# View for Course
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related("tutor").all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerTutorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # فیلترهای نمونه
    filterset_fields = ['language', 'level', 'schedule_day']
    search_fields = ['title', 'description', 'detail']
    ordering_fields = ['price_per_hour', 'price_per_dollar', 'price_per_toman', 'title']
    ordering = ['title']

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated or not hasattr(user, "tutor"):
            raise PermissionDenied("Only tutors can create courses.")
        serializer.save(tutor=user.tutor)

    def perform_update(self, serializer):
        # پرمیشن کلاس هم چک می‌کند، ولی اینجا هم مالکیت را enforce می‌کنیم
        course = self.get_object()
        if not hasattr(self.request.user, "tutor") or course.tutor != self.request.user.tutor:
            raise PermissionDenied("You can edit only your own courses.")
        serializer.save()

# View for Tutor
class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    permission_classes = [AllowAny]

# View for Student
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

# View for Lesson
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]

# View for Homework
class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [IsAuthenticated]

# View for Review
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


