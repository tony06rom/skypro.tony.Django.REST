from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson


class LessonShortSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "title")


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonShortSerializer(source="lesson_set", many=True, read_only=True)

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
