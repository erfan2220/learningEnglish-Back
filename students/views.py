# students/views.py
from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer  # Correct import

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
