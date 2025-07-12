from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient, APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonsAPIViewTestCase(APITestCase):
    def setUp(self):
        Group.objects.create(name="moderators")
        self.user = User.objects.create_user(email="user_1@mail.ru", password="qwerty12345")
        self.user_2 = User.objects.create_user(email="user_2@mail.ru", password="qwerty12345")
        self.moder = User.objects.create_user(email="moder@mail.ru", password="qwerty12345")
        self.moder.groups.add(Group.objects.get(name="moderators"))
        Course.objects.create(id=1, title="course_1", description="description_1")
        self.client = APIClient()
        self.lesson = Lesson.objects.create(
            title="lesson_1",
            description="description_1",
            video_url="https://youtube.com/video_1",
            course=Course.objects.get(id=1),
            owner=User.objects.first(),
        )

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(
            title="lesson_2",
            description="description_2",
            video_url="https://youtube.com/video_1",
            course=Course.objects.get(id=1),
            owner=User.objects.first(),
        )
        url = reverse("lms:lesson_delete", kwargs={"pk": lesson.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lesson_owner(self):
        lesson = Lesson.objects.create(
            title="lesson_2",
            description="description_2",
            video_url="https://youtube.com/video_1",
            course=Course.objects.get(id=1),
            owner=User.objects.first(),
        )
        url = reverse("lms:lesson_delete", kwargs={"pk": lesson.pk})
        self.client.force_authenticate(user=self.user_2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lesson_unauthenticated(self):
        lesson = Lesson.objects.create(
            title="lesson_2",
            description="description_2",
            video_url="https://youtube.com/video_1",
            course=Course.objects.get(id=1),
            owner=User.objects.first(),
        )
        url = reverse("lms:lesson_delete", kwargs={"pk": lesson.pk})
        self.client.force_authenticate(user=None)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_lesson_by_moder(self):
        lesson = Lesson.objects.create(
            title="lesson_2",
            description="description_2",
            video_url="https://youtube.com/video_1",
            course=Course.objects.get(id=1),
            owner=User.objects.first(),
        )
        url = reverse("lms:lesson_delete", kwargs={"pk": lesson.pk})
        self.client.force_authenticate(user=self.moder)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list(self):
        url = reverse("lms:lesson_list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_list_unauthenticated(self):
        url = reverse("lms:lesson_list")
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_create(self):
        url = reverse("lms:lesson_create")
        data = {
            "title": "lesson_1",
            "description": "description_1",
            "video_url": "https://youtube.com/video_1",
            "course": 1,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "lesson_1")
        self.assertEqual(Lesson.objects.all().count(), 2)

        # Проверка поля video_url
        data = {
            "title": "lesson_1",
            "description": "description_1",
            "video_url": "https://vk.com/video_1",
            "course": 1,
        }
        self.client.force_authenticate(user=self.user)
        self.client.post(url, data)
        self.assertRaises(ValidationError)

    def test_lesson_create_by_moder(self):
        url = reverse("lms:lesson_create")
        data = {
            "title": "lesson_1",
            "description": "description_1",
            "video_url": "https://youtube.com/video_1",
            "course": 1,
        }
        self.client.force_authenticate(user=self.moder)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_create_unauthenticated(self):
        url = reverse("lms:lesson_create")
        data = {
            "title": "lesson_1",
            "description": "description_1",
            "video_url": "https://youtube.com/video_1",
            "course": 1,
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_partial_update(self):
        url = reverse("lms:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {"title": "patch_lesson"}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "patch_lesson")
        self.client.force_authenticate(user=self.moder)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "patch_lesson")

    def test_lesson_partial_update_unauthenticated(self):
        url = reverse("lms:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {"title": "patch_lesson"}
        self.client.force_authenticate(user=None)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_partial_update_owner(self):
        url = reverse("lms:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {"title": "patch_lesson"}
        self.client.force_authenticate(user=self.user_2)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_full_update(self):
        url = reverse("lms:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {
            "title": "put_lesson",
            "description": "put_lesson",
            "video_url": "https://youtube.com/video_1",
            "course": 1,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "put_lesson")

    def test_lesson_full_update_unauthenticated(self):
        url = reverse("lms:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {
            "title": "put_lesson",
            "description": "put_lesson",
            "video_url": "https://youtube.com/video_1",
            "course": 1,
        }
        self.client.force_authenticate(user=None)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_full_update_owner(self):
        url = reverse("lms:lesson_update", kwargs={"pk": self.lesson.pk})
        data = {
            "title": "put_lesson",
            "description": "put_lesson",
            "video_url": "https://youtube.com/video_1",
            "course": 1,
        }
        self.client.force_authenticate(user=self.user_2)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@mail.ru", password="qwerty12345")
        self.course = Course.objects.create(id=1, title="course_1", description="description_1")
        self.client = APIClient()
        self.url = reverse("lms:course_subscribe", kwargs={"pk": self.course.pk})

    def test_subscription(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, {"pk": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "подписка активирована")
        self.assertEqual(Subscription.objects.all().count(), 1)

        response = self.client.post(self.url, {"pk": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "подписка деактивирована")
        self.assertEqual(Subscription.objects.all().count(), 0)

    def test_subscription_create_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, {"pk": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
