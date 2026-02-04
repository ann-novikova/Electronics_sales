from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Generic для создания пользователя"""

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Метод, который вызывается во время создания нового объекта через API"""
        user = serializer.save()
        password = serializer.validated_data.get("password")
        user.set_password(password)
        user.is_active = True
        user.save()
