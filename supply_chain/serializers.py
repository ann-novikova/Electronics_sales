from rest_framework import serializers

from supply_chain.models import ChainNode, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'release_date', 'chain_node']


class ChainNodeSerializer(serializers.ModelSerializer):
    """сериализатор для звена сети"""

    level_display = serializers.CharField(source="get_level_display", read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    products_count = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ChainNode
        fields = [
            "id",
            "name",
            "level",
            "level_display",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
            "debt",
            "products",
            "products_count",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_products_count(self, obj):
        """Возвращает количество продуктов у звена сети"""
        return obj.products.count()

    def update(self, instance, validated_data):
        # Запрет на обновление поля debt_to_supplier через API (как требование).
        if 'debt' in validated_data:
            validated_data.pop('debt')
        return super().update(instance, validated_data)

    def validate(self, data):
        """Валидация данных при создании"""
        level = data.get("level")
        supplier = data.get("supplier")

        # Завод не может иметь поставщика
        if level == 0 and supplier:
            raise serializers.ValidationError(
                {"supplier": "Завод не может иметь поставщика"}
            )

        if level in [1, 2] and not supplier:
            raise serializers.ValidationError(
                {"supplier": "Розничная сеть и ИП должны иметь поставщика"}
            )

        if supplier:
            current = supplier
            while current:
                if current == data.get("instance"):
                    raise serializers.ValidationError(
                        {
                            "supplier": "Обнаружена циклическая зависимость в цепочке поставщиков"
                        }
                    )
                current = current.supplier

        return data

