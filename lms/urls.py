from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import (CourseSubscribeAPIView, CourseViewSet, LessonCreateAPIView, LessonDestroyAPIView,
                       LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView)

app_name = LmsConfig.name

router = SimpleRouter()
router.register(r"course", CourseViewSet, basename="course")

urlpatterns = [
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
    path("lesson/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("courses/<int:pk>/subscribe/", CourseSubscribeAPIView.as_view(), name="course_subscribe"),
] + router.urls
