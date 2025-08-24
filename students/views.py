# students/views.py
from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer  # Correct import
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from courses.models import Course


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=True, methods=['post'], url_path='add-course')
    def add_course(self, request, pk=None):
        student = self.get_object()
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({'error': 'Course ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(pk=course_id)

            # Check if the course is already added
            if student.courses_list.filter(id=course.id).exists():
                return Response({'error': 'Course already added to student'}, status=status.HTTP_400_BAD_REQUEST)

            student.courses_list.add(course)
            student.save()  # Save the student instance after adding the course

            return Response({
                'status': 'course added',
                'courses_list': CourseSerializer(student.courses_list.all(), many=True).data
            }, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
