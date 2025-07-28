from django.db import models
from tutors.models import Tutor
from accounts.models import User  # Add the import for User model

# Course Model
class Course(models.Model):
    tutor = models.ForeignKey(Tutor, related_name='tutored_courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    courseId = models.CharField(default='cr1001', max_length=20, unique=True)
    description = models.TextField(default='Default course description')
    detail = models.TextField(default='Default course detail')
    requirements = models.TextField(default='Default course req')
    materials = models.TextField(default='Default course mat')


    price_per_hour = models.DecimalField(default=10, max_digits=10, decimal_places=2)
    price_per_dollar = models.DecimalField(default=12, max_digits=10, decimal_places=2)
    price_per_toman = models.DecimalField(default=960, max_digits=10, decimal_places=2)


    language = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    schedule_day = models.CharField(max_length=50)
    schedule_start = models.TimeField()
    schedule_end = models.TimeField()


    capacity = models.IntegerField()
    active_students = models.IntegerField(default=0)
    length = models.IntegerField(default=20)
    course_duration = models.IntegerField(default=60)


    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    language_flag = models.ImageField(upload_to='flags/', null=True, blank=True)

    def __str__(self):
        return self.title

# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses_list = models.ManyToManyField(Course, related_name="students")
    favorite_tutors = models.ManyToManyField(Tutor, related_name="favorite_students")
    student_active = models.BooleanField(default=True)
    student_homework_completed = models.JSONField()

    def __str__(self):
        return self.user.first_name

# Lesson Model
class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    lesson_video = models.URLField(null=True, blank=True)
    lesson_document = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

# Homework Model
class Homework(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='homeworks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    document = models.URLField(null=True, blank=True)
    due_date = models.DateField()

    def __str__(self):
        return self.title


# Review Model (for reviews from students to tutors)
class Review(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField()  # Rating out of 5
    review_date = models.DateField()

    def __str__(self):
        return f"Review by {self.student.user.first_name} for {self.tutor.user.first_name}"

