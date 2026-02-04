from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class UserTestCase(APITestCase):
    """Определяем класс тестирования методов пользователя"""

    def setUp(self):
        """Определяем настройки"""

        self.email = "test@mail.ru"
        self.password = "12345"

    def test_user_registration(self):
        """Тестирование регистрации пользователя"""

        data = {
            "email": self.email,
            "password": self.password,
        }
        response = self.client.post("/users/register/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test@mail.ru").exists())
