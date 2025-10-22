# # tutors/views.py
# from rest_framework import viewsets, permissions
# from .models import Tutor,TutorCourse,TutorCertificate, TutorEducation, TutorExperience
# from .serializers import (
#     TutorSerializer,
#     TutorCourseSerializer,
#     TutorCertificateSerializer,
#     TutorEducationSerializer,
#     TutorExperienceSerializer,
# )
#
#
#
# class ReadOnlyOrAuth(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # allow anyone to GET/HEAD/OPTIONS; require auth for POST/PUT/PATCH/DELETE
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return request.user and request.user.is_authenticated
#
#
# class CreateTutorProfileView(APIView):
#     permission_classes = [permissions.IsAuthenticated]   # must be logged in
#     parser_classes = [MultiPartParser, FormParser, JSONParser]  # supports files + json
#
#     def post(self, request):
#         data = request.data.copy()
#
#         # Accept both JSON arrays and stringified arrays for JSONFields:
#         for key in ("languages_spoken", "subjects"):
#             val = data.get(key)
#             if isinstance(val, str):
#                 try:
#                     data[key] = json.loads(val)
#                 except json.JSONDecodeError:
#                     # If comma-separated string is sent, split it
#                     data[key] = [s.strip() for s in val.split(",") if s.strip()]
#
#         serializer = TutorSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#
#         # attach the current user
#         serializer.save(user=request.user)

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
#
# class TutorViewSet(viewsets.ModelViewSet):
#     queryset = Tutor.objects.select_related("user").prefetch_related(
#         "certificates", "educations", "experiences","courses"
#     )
#     serializer_class = TutorSerializer
#     permission_classes = [ReadOnlyOrAuth]
#
# class TutorCourseViewSet(viewsets.ModelViewSet):
#     queryset = TutorCourse.objects.all()
#     serializer_class = TutorCourseSerializer
#     permission_classes = [ReadOnlyOrAuth]
#
# class TutorCertificateViewSet(viewsets.ModelViewSet):
#     queryset = TutorCertificate.objects.all()
#     serializer_class = TutorCertificateSerializer
#     permission_classes = [ReadOnlyOrAuth]
#
# class TutorEducationViewSet(viewsets.ModelViewSet):
#     queryset = TutorEducation.objects.all()
#     serializer_class = TutorEducationSerializer
#     permission_classes = [ReadOnlyOrAuth]
#
# class TutorExperienceViewSet(viewsets.ModelViewSet):
#     queryset = TutorExperience.objects.all()
#     serializer_class = TutorExperienceSerializer
#     permission_classes = [ReadOnlyOrAuth]


import json
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Tutor, TutorCertificate, TutorEducation, TutorExperience, TutorCourse

from .logging import logger

from .serializers import (
    TutorSerializer,
    TutorCourseSerializer,
    TutorCertificateSerializer,
    TutorEducationSerializer,
    TutorExperienceSerializer,
    CreateTutorProfileInputSerializer,
)

class ReadOnlyOrAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        return True if request.method in permissions.SAFE_METHODS else bool(request.user and request.user.is_authenticated)

# ViewSets (browse/edit pieces)
class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.select_related("user").prefetch_related("certificates", "educations", "experiences", "courses")
    serializer_class = TutorSerializer
    permission_classes = [ReadOnlyOrAuth]

class TutorCourseViewSet(viewsets.ModelViewSet):
    queryset = TutorCourse.objects.all()
    serializer_class = TutorCourseSerializer
    permission_classes = [ReadOnlyOrAuth]

class TutorCertificateViewSet(viewsets.ModelViewSet):
    queryset = TutorCertificate.objects.all()
    serializer_class = TutorCertificateSerializer
    permission_classes = [ReadOnlyOrAuth]

class TutorEducationViewSet(viewsets.ModelViewSet):
    queryset = TutorEducation.objects.all()
    serializer_class = TutorEducationSerializer
    permission_classes = [ReadOnlyOrAuth]

class TutorExperienceViewSet(viewsets.ModelViewSet):
    queryset = TutorExperience.objects.all()
    serializer_class = TutorExperienceSerializer
    permission_classes = [ReadOnlyOrAuth]
# ----------------------------------------
# Create (one-shot or page-by-page) endpoint
# ----------------------------------------
class CreateTutorProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @extend_schema(request=CreateTutorProfileInputSerializer, responses={201: TutorSerializer})
    def post(self, request):
        qd = request.data  # QueryDict
        logger.debug(f"Received data: {qd}")

        def first_or_none(key):
            """Get first value from QueryDict list (files supported)."""
            try:
                vals = qd.getlist(key)
            except AttributeError:
                # Not a QueryDict (e.g., JSON body) — return as-is
                return qd.get(key)
            if not vals:
                return None
            return vals[0]

        def looks_like_json(s: str) -> bool:
            s = s.strip()
            return (s.startswith("[") and s.endswith("]")) or (s.startswith("{") and s.endswith("}"))

        def strip_outer_quotes_if_wrapped(s: str) -> str:
            # turns '"["Chinese"]"' -> '["Chinese"]'
            s = s.strip()
            if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
                inner = s[1:-1].strip()
                # only strip if the inner looks like JSON to avoid breaking normal strings
                if looks_like_json(inner):
                    return inner
            return s

        # Build a plain dict payload
        payload = {}

        # Simple text fields
        for key in ["first_name", "last_name", "phone_number", "country",
                    "bio", "teaching_style", "expectation", "description",
                    "intro_video_url"]:
            val = first_or_none(key)
            if val is not None:
                payload[key] = val

        # File fields
        for key in ["profile_picture", "intro_video_file"]:
            f = first_or_none(key)
            if f is not None:
                payload[key] = f

        # JSON/list-ish fields that may arrive as strings (sometimes double-quoted)
        jsonish_keys = ["subjects", "languages_spoken", "certificates", "educations", "experiences", "courses"]
        for key in jsonish_keys:
            raw = first_or_none(key)
            if raw is None:
                continue

            # If already a Python obj (e.g., pure JSON body), keep it
            if isinstance(raw, (list, dict)):
                obj = raw
            else:
                s = str(raw)
                s = strip_outer_quotes_if_wrapped(s)  # remove accidental extra quotes
                if looks_like_json(s):
                    try:
                        obj = json.loads(s)
                    except json.JSONDecodeError:
                        obj = s
                else:
                    obj = s

            # Special handling per field
            if key == "subjects":
                # Accept: list => ensure flat list of strings
                if isinstance(obj, list):
                    # If it’s a list with one string that is JSON, parse it
                    if len(obj) == 1 and isinstance(obj[0], str) and looks_like_json(obj[0].strip()):
                        try:
                            obj = json.loads(obj[0].strip())
                        except json.JSONDecodeError:
                            pass
                    # Flatten any nested lists; coerce items to strings
                    flat = []
                    for item in obj:
                        if isinstance(item, list):
                            flat.extend([str(x) for x in item])
                        else:
                            flat.append(str(item))
                    obj = flat
                elif isinstance(obj, str):
                    # support "English,Chinese" as fallback
                    if looks_like_json(obj):
                        try:
                            obj = json.loads(obj)
                        except json.JSONDecodeError:
                            obj = [obj]
                    else:
                        obj = [s.strip() for s in obj.split(",") if s.strip()]
                else:
                    obj = []

            payload[key] = obj

        logger.debug(f"Normalized payload: {payload}")

        # Validate
        ser_in = CreateTutorProfileInputSerializer(data=payload, partial=True)
        try:
            ser_in.is_valid(raise_exception=True)
        except Exception as e:
            logger.exception("Validation error in CreateTutorProfileInputSerializer")
            return Response({"detail": ser_in.errors}, status=status.HTTP_400_BAD_REQUEST)

        v = ser_in.validated_data

        # Prevent duplicate tutor profiles
        if Tutor.objects.filter(user=request.user).exists():
            return Response({"detail": "Tutor profile already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Update user names if provided
        updates = []
        if "first_name" in v:
            request.user.first_name = v["first_name"]; updates.append("first_name")
        if "last_name" in v:
            request.user.last_name = v["last_name"]; updates.append("last_name")
        if updates:
            request.user.save(update_fields=updates)

        # Create Tutor
        tutor = Tutor.objects.create(
            user=request.user,
            profile_picture=v.get("profile_picture"),
            languages_spoken=v.get("languages_spoken", []),
            country=v.get("country", ""),
            subjects=v.get("subjects", []),
            phone_number=v.get("phone_number", ""),
            bio=v.get("bio", ""),
            teaching_style=v.get("teaching_style", ""),
            expectation=v.get("expectation", ""),
            # description=v.get("description", ""),
            intro_video_url=v.get("intro_video_url", ""),
            intro_video_file=v.get("intro_video_file"),
        )

        # Nested creates
        for c in v.get("certificates", []):
            TutorCertificate.objects.create(
                tutor=tutor,
                title=c["title"],
                issued_by=c.get("issued_by", ""),
                issue_date=c.get("issue_date"),
                certificate_image=c.get("certificate_image"),
            )

        for e in v.get("educations", []):
            TutorEducation.objects.create(
                tutor=tutor,
                degree=e["degree"],
                institution_name=e["institution_name"],
                country=e.get("country", ""),
                city=e.get("city", ""),
                field=e.get("field", ""),
                start_date=e.get("start_date"),
                end_date=e.get("end_date"),
            )

        for ex in v.get("experiences", []):
            TutorExperience.objects.create(
                tutor=tutor,
                title=ex["title"],
                organization=ex.get("organization", ""),
                country=ex.get("country", ""),
                city=ex.get("city", ""),
                start_date=ex.get("start_date"),
                end_date=ex.get("end_date"),
                description=ex.get("description", ""),
            )

        for course in v.get("courses", []):
            TutorCourse.objects.create(
                tutor=tutor,
                course_title=course["course_title"],
                duration_minutes=course["duration_minutes"],
                course_type=course["course_type"],
                price_per_hour=course["price_per_hour"],
                lesson_package=course["lesson_package"],
                language=course["language"],
                days_available=course.get("days_available", []),
                time_slots=course.get("time_slots", []),
                start_date=course["start_date"],
                description=course["description"],
            )

        return Response(TutorSerializer(tutor).data, status=status.HTTP_201_CREATED)