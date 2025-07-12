from rest_framework import serializers
from .models import Tutor
from accounts.models import User

class TutorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Tutor
        fields = ['user', 'profile_picture', 'languages']
