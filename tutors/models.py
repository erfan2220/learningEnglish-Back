from django.db import models
from accounts.models import User

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tutor')  # Changed related_name
    profile_picture = models.ImageField(upload_to='tutor_photos/', null=True, blank=True)
    languages_spoken = models.JSONField()  # List of languages tutor speaks and their proficiency level

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"