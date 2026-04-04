from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Course, Lesson, CourseSubscription

User = get_user_model()


class CourseTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpass123'
        )
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass'
        )
        self.course = Course.objects.create(
            title="Test Course",
            owner=self.user
        )

    def test_create_course_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/courses/',
                                    {'title': 'New Course', 'description': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_own_course(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/api/courses/{self.course.id}/',
                                     {'title': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_other_course_forbidden(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(f'/api/courses/{self.course.id}/',
                                     {'title': 'Hack'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subscribe_unsubscribe(self):
        self.client.force_authenticate(user=self.user)
        # Подписка
        response = self.client.post(f'/api/courses/{self.course.id}/subscribe/')
        self.assertEqual(response.data['message'], 'Подписка добавлена')

        # Отписка
        response = self.client.post(f'/api/courses/{self.course.id}/subscribe/')
        self.assertEqual(response.data['message'], 'Подписка удалена')