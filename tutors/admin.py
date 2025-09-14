# tutors/admin.py
from django.contrib import admin
from .models import Tutor, TutorCertificate, TutorEducation, TutorExperience

class TutorCertificateInline(admin.StackedInline):
    model = TutorCertificate
    extra = 0

class TutorEducationInline(admin.StackedInline):
    model = TutorEducation
    extra = 0
#/admin.py
class TutorExperienceInline(admin.StackedInline):
    model = TutorExperience
    extra = 0

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "country", "phone_number")
    search_fields = ("user__first_name", "user__last_name", "user__email", "country")
    inlines = [TutorCertificateInline, TutorEducationInline, TutorExperienceInline]

admin.site.register(TutorCertificate)
admin.site.register(TutorEducation)
admin.site.register(TutorExperience)
