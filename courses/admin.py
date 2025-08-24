from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title","courseId","tutor","language","level","price_per_hour","capacity","active_students")
    search_fields = ("title","courseId","tutor__user__first_name","tutor__user__last_name","language","level")
    list_filter = ("language","level","schedule_day")