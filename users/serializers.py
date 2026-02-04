from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор класса пользователя"""

    class Meta:
        model = User
        fields = ["id", "email", "password"]
