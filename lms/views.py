from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Subscription
from lms.pagination import CustomPagination
from lms.permissions import IsModerator, IsNotModerator, IsOwner
from lms.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsNotModerator,)
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsNotModerator | IsOwner,)
        return super().get_permissions()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    pagination_class = CustomPagination


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsNotModerator]


class CourseSubscribeAPIView(APIView):
    def post(self, request, pk):
        user = request.user
        course_item = Course.objects.get(pk=pk)
        try:
            subs_item = Subscription.objects.get(user=user, course=course_item)
        except Subscription.DoesNotExist:
            sub = Subscription.objects.create(user=user, course=course_item)
            sub.save()
            return Response({"message": "подписка активирована"}, status=status.HTTP_201_CREATED)
        else:
            subs_item.delete()
            return Response({"message": "подписка деактивирована"}, status=status.HTTP_201_CREATED)
