from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from .models import Author, Book, Order
from .serializers import OrderSerializer


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', password='p')
        self.author = Author.objects.create(
            name='Author', bio='Bio', birth_date='1990-01-01'
        )
        self.book = Book.objects.create(
            title='Book', author=self.author, price=10, stock=5, published_date='2020-01-01'
        )

    def test_total_price_calculated(self):
        order = Order.objects.create(user=self.user, book=self.book, quantity=2)
        self.assertEqual(order.total_price, 20)

    def test_stock_reduced(self):
        Order.objects.create(user=self.user, book=self.book, quantity=2)
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 3)

class OrderSerializerTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='A', bio='B', birth_date='1990-01-01')
        self.book = Book.objects.create(
            title='Book', author=self.author, price=10, stock=2, published_date='2020-01-01'
        )

    def test_quantity_exceeds_stock(self):
        serializer = OrderSerializer(data={'book': self.book.id, 'quantity': 5})
        self.assertFalse(serializer.is_valid())

class OrderAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='u', password='p')
        self.author = Author.objects.create(name='A', bio='B', birth_date='1990-01-01')
        self.book = Book.objects.create(
            title='Book', author=self.author, price=10, stock=5, published_date='2020-01-01'
        )

    def test_create_order_unauthenticated(self):
        response = self.client.post('/api/orders/', {'book': self.book.id, 'quantity': 1})
        self.assertEqual(response.status_code, 403)

    def test_create_order_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/orders/', {'book': self.book.id, 'quantity': 1})
        self.assertEqual(response.status_code, 201)

