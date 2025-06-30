from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class Subject (models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name



class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='tutor_profile')
    bio = models.TextField()
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    subjects = models.ManyToManyField(Subject)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    is_verified=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.name}'s Tutor Profile"

class Availability(models.Model):
        tutor =models.ForeignKey(TutorProfile, on_delete=models.CASCADE , related_name='availabilities')
        days_of_week=models.PositiveSmallIntegerField(
            choices=[(0, 'Monday'), (1, 'Tuesday'),(2, 'Wednesday'),
                     (3, 'Thursday'),(4, 'Friday'),(5, 'Saturday'),(6, 'Sunday')])
        start_time= models.TimeField()
        end_time= models.TimeField()


        class Meta:
            verbose_name_plural = "Availabilities"
            ordering = ['day_of_week','start_time']

            def __str__(self):
                return f"{self.tutor.user.username} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"

class Lesson(models.Model):
            tutor=models.ForeignKey(TutorProfile, on_delete=models.CASCADE , related_name='lessons')
            student = models.ForeignKey(User, on_delete=models.CASCADE , related_name='lessons')

            subject = models.ForeignKey(Subject, on_delete=models.SET_NULL , null=True)

            start_time = models.DateTimeField()
            end_time = models.DateTimeField()

            status = models.CharField(max_length=20,
                                      choices=[
                                          ('pending', 'Pending'),
                                          ('confirmed', 'Confirmed'),
                                          ('completed', 'Completed'),
                                          ('cancelled', 'Cancelled'),
                                      ],
                                      default='pending'
                                      )

            meeting_url = models.URLField(blank=True, null=True)
            created_at = models.DateTimeField(auto_now_add=True)

            class Meta:
                ordering = ['start_time']

                def __str__(self):
                    return f"{self.student.username} with {self.tutor.user.username} on {self.start_time}"


class Review(models.Model):
                lesson= models.OneToOneField(Lesson, on_delete=models.CASCADE , related_name='review')
                rating = models.PositiveIntegerField(
                    validators=[MinValueValidator(1), MaxValueValidator(5)]
                )

                comment = models.TextField(blank=True)
                created_at = models.DateTimeField(auto_now_add=True)

                def __str__(self):
                    return f"{self.rating} stars for {self.lesson.tutor.user.username}"







