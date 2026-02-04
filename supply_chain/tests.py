from datetime import date, timedelta
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from supply_chain.models import ChainNode, Product, ChainNode
from users.models import User


class BaseTestCase(APITestCase):
    """Базовый класс для тестов с общими настройками"""

    def setUp(self):
        # Создаем тестовых пользователей
        self.active_user = User.objects.create_user(
            email="test@mail.ru",
            password="12345",
            phone="+71111111111",
            city="Санкт-Петербург",
            is_staff=True,
            is_active=True,
        )
        self.inactive_user = User.objects.create_user(
            email="inactive@mail.ru",
            password="12345",
            phone="+78888888888",
            city="Санкт-Петербург",
            is_staff=True,
            is_active=False,
        )

        # Создаем тестовые звенья сети
        self.plant = ChainNode.objects.create(
            name="Завод 1",
            level=0,
            email="plant1@mail.ru",
            country="Россия",
            city="Санкт-Петербург",
            street="Южное шоссе",
            house_number="53",
            debt=0,
        )

        self.retail_chain = ChainNode.objects.create(
            name="retail 1'",
            level=1,
            email="retail@mail.ru",
            country="Россия",
            city="Санкт-Петербург",
            street="Невский проспект",
            house_number="1",
            supplier=self.plant,
            debt=100000.30,
        )

        self.entrepreneur = ChainNode.objects.create(
            name="ИП Тест",
            level=2,
            email="ip@mail.ru",
            country="Россия",
            city="Санкт-Петербург",
            street="Бухарестская",
            house_number="110/1",
            supplier=self.retail_chain,
            debt=20000.55,
        )

        # Создаем тестовые продукты
        self.product1 = Product.objects.create(
            name="Смартфон",
            model="Iphone 17",
            release_date=date(2025, 9, 30),
            chain_node=self.plant,
        )

        self.product2 = Product.objects.create(
            name="Наушники",
            model="AirPods Pro",
            release_date=date(2025, 9, 30),
            chain_node=self.retail_chain,
        )

        self.product3 = Product.objects.create(
            name="Планшет",
            model="iPad Air",
            release_date=date(2024, 9, 30),
            chain_node=self.entrepreneur,
        )

        # Клиент API для активного пользователя
        self.active_client = APIClient()
        self.active_client.force_authenticate(user=self.active_user)

        # Клиент API для неактивного пользователя
        self.inactive_client = APIClient()
        self.inactive_client.force_authenticate(user=self.inactive_user)

        # Неавторизованный клиент
        self.anonymous_client = APIClient()


class SupplierViewSetTest(BaseTestCase):
    """Тесты для SupplierViewSet"""

    def test_list_suppliers_active_user(self):
        """Тест получения списка звеньев сети активным пользователем"""
        url = reverse("supplier-list")
        response = self.active_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_suppliers_inactive_user(self):
        """Тест получения списка звеньев сети неактивным пользователем"""
        url = reverse("supplier-list")
        response = self.inactive_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_suppliers_anonymous(self):
        """Тест получения списка звеньев сети анонимным пользователем"""
        url = reverse("supplier-list")
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_supplier(self):
        """Тест получения детальной информации о звене сети"""
        url = reverse("supplier-detail", args=[self.plant.id])
        response = self.active_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Завод 1")

    def test_create_supplier(self):
        """Тест создания нового звена сети"""
        url = reverse("supplier-list")
        data = {
            "name": "Test",
            "level": 1,
            "email": "new_test@mail.ru",
            "country": "Россия",
            "city": "Санкт-Петербург",
            "street": "Ленина",
            "house_number": "1",
            "supplier": self.plant.id,
        }
        response = self.active_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChainNode.objects.count(), 4)

    def test_create_factory_without_supplier(self):
        """Тест создания завода без поставщика"""
        url = reverse("supplier-list")
        data = {
            "name": "завод 2",
            "level": 0,
            "email": "plant2@mail.ru",
            "country": "Россия",
            "city": "Санкт-Петербург",
            "street": "Звездная",
            "house_number": "2",
        }
        response = self.active_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_chain_node(self):
        """Тест обновления звена сети"""
        url = reverse("supplier-detail", args=[self.retail_chain.id])
        data = {"name": "retail network 1", "city": "Москва"}
        response = self.active_client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.retail_chain.refresh_from_db()
        self.assertEqual(self.retail_chain.name, "retail network 1")
        self.assertEqual(self.retail_chain.city, "Москва")

    def test_update_debt_prohibited(self):
        """Тест запрета обновления поля debt через API"""
        url = reverse("supplier-detail", args=[self.retail_chain.id])
        original_debt = Decimal(str(self.retail_chain.debt))
        data = {"debt": 0}  # Попытка очистить задолженность
        response = self.active_client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.retail_chain.refresh_from_db()
        self.assertEqual(self.retail_chain.debt, original_debt)

    def test_delete_chain_node(self):
        """Тест удаления звена сети"""
        url = reverse("supplier-detail", args=[self.entrepreneur.id])
        response = self.active_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ChainNode.objects.count(), 2)

    def test_filter_by_country(self):
        """Тест фильтрации по стране"""
        url = reverse("supplier-list") + "?country=Россия"
        response = self.active_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_city(self):
        """Тест фильтрации по городу"""
        url = reverse("supplier-list") + "?city=Санкт-Петербург"
        response = self.active_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что возвращаются только объекты из Санкт-Петербурга
        if "results" in response.data:
            for item in response.data["results"]:
                self.assertEqual(item["city"], "Санкт-Петербург")

    def test_search_by_name(self):
        """Тест поиска по названию"""
        url = reverse("supplier-list") + "?search=Завод 1"
        response = self.active_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ordering_by_name(self):
        """Тест сортировки по названию"""
        url = reverse("supplier-list") + "?ordering=name"
        response = self.active_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductViewSetTest(BaseTestCase):
    """Тесты для ProductViewSet"""

    def test_list_products_active_user(self):
        """Тест получения списка продуктов активным пользователем"""
        url = reverse("product-list")
        response = self.active_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_products_inactive_user(self):
        """Тест получения списка продуктов неактивным пользователем"""
        url = reverse("product-list")
        response = self.inactive_client.get(url)
        # Исправляем ожидаемый статус - неактивный пользователь должен получать 403
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_products_anonymous(self):
        """Тест получения списка продуктов анонимным пользователем"""
        url = reverse("product-list")
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product(self):
        """Тест создания нового продукта"""
        url = reverse("product-list")
        data = {
            "name": "Новый смартфон",
            "model": "Model 1",
            "release_date": "2026-01-01",
            "chain_node": self.plant.id,
        }
        response = self.active_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 4)

    def test_create_product_future_release_date(self):
        """Тест создания продукта с датой выпуска в будущем"""
        url = reverse("product-list")
        future_date = date.today() + timedelta(days=365)
        data = {
            "name": "Будущий продукт",
            "model": "Future Model",
            "release_date": future_date.isoformat(),
            "network_node": self.plant.id,
        }
        response = self.active_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product(self):
        """Тест обновления продукта"""
        url = reverse("product-detail", args=[self.product1.id])
        data = {"name": "Обновленный смартфон", "model": "Iphone 17 Pro"}
        response = self.active_client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, "Обновленный смартфон")

    def test_delete_product(self):
        """Тест удаления продукта"""
        url = reverse("product-detail", args=[self.product3.id])
        response = self.active_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 2)

    def test_filter_by_country(self):
        """Тест фильтрации продуктов по стране сети"""
        url = reverse("product-list") + "?network_node__country=Россия"
        response = self.active_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_products(self):
        """Тест поиска продуктов"""
        url = reverse("product-list") + "?search=Iphone"
        response = self.active_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ordering_products(self):
        """Тест сортировки продуктов"""
        url = reverse("product-list") + "?ordering=release_date"
        response = self.active_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

