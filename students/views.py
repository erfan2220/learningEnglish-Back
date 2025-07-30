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

    @action(detail=True, methods=['post'],url_path='add-course')
    def add_course(self,request,pk=None):
        student = self.get_object()
        course_id = request.data.get('course_id')
        try:
            course = Course.objects.get(courseId=course_id)
            student.courses_list.add(course)
            return Response({'status': 'course added'}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
