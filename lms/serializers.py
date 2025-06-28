from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = SerializerMethodField()

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()

    def get_lessons(self, instance):
        lessons = instance.lesson_set.all()
        return [{'id': lesson.id, 'title': lesson.title} for lesson in lessons]

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
