from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import UrlValidator


class LessonShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "title")


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonShortSerializer(source="lesson_set", many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()

    # def get_subscription(self, instance):
    #     sub = Subscription.objects.get(course=instance)
    #     return sub.user == self.context["request"].user

    def get_subscription(self, instance):
        try:
            sub = Subscription.objects.get(course=instance)
            return sub.user == self.context["request"].user
        except ObjectDoesNotExist:
            return False

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field='video_url')]
