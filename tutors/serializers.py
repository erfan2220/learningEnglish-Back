# tutors/serializers.py
from rest_framework import serializers
from .models import Tutor,TutorCourse,TutorCertificate, TutorEducation, TutorExperience
from accounts.models import User

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]

class TutorCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorCourse
        fields = "__all__"

class TutorCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorCertificate
        fields = "__all__"

class TutorEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorEducation
        fields = "__all__"

class TutorExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorExperience
        fields = "__all__"

class TutorSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    certificates = TutorCertificateSerializer(many=True, read_only=True)
    educations = TutorEducationSerializer(many=True, read_only=True)
    experiences = TutorExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Tutor
        fields = [
            "id", "user", "profile_picture", "languages_spoken",
            "country", "subjects", "phone_number", "bio",
            "intro_video_url", "intro_video_file",
            "certificates", "educations", "experiences",
        ]
