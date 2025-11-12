from django.contrib.auth.models import User
from django.test import TestCase

from decimal import Decimal
from myapp.models import Product
from rest_framework import status
from rest_framework.test import APITestCase


class ProductTests(TestCase):
    def test_price_with_vat(self):
        product = Product(name='Phone', price=Decimal('100.00'))
        self.assertEqual(product.price_with_vat, Decimal('120.00'))

    def test_apply_discount(self):
        product = Product(name='Phone', price=Decimal('500.00'))
        discounted = product.apply_discount(10)
        self.assertEqual(discounted, 450.00)


class ProductIntegrationTests(APITestCase):
    def test_create_product(self):
        data = {'name': 'Laptop', 'price': '1000.00'}
        response = self.client.post('/api/products/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name='Laptop').exists())

    def test_create_product_price_incorrect(self):
        data = {'name': 'Laptop', 'price': '-1000.00'}
        response = self.client.post('/api/products/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductListTests(APITestCase):
    def test_get_products(self):
        Product.objects.create(name='Phone', price='500')
        response = self.client.get('/api/products/')
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Phone', str(response.data))


class ProductBlackBoxTests(APITestCase):
    def test_create_product(self):
        data = {'name': 'Laptop', 'price': '1000.00'}
        response = self.client.post('/api/products/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProductWhiteBoxTests(TestCase):
    def test_price_with_vat_calculation(self):
        product = Product(name='Phone', price=Decimal('100.00'))
        result = product.price_with_vat
        self.assertEqual(result, Decimal('120.00'))


class ProductModelTest(TestCase):
    def test_crud_operations(self):
        product = Product.objects.create(name="Tablet", price=1000)
        self.assertEqual(Product.objects.count(), 1)

        product.price = 900
        product.save()
        self.assertEqual(Product.objects.get(pk=product.pk).price, 900)

        product.delete()
        self.assertEqual(Product.objects.count(), 0)


class ProductViewTests(TestCase):
    def test_product_detail_found(self):
        product = Product.objects.create(name="Mac Book", price=100)
        response = self.client.get(f'/api/products/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Mac Book', response.json()['name'])

    def test_redirect_after_register(self):
        response = self.client.post('/register/', {
            'username': 'user',
            'password': '123',
            'password2': '123',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('', response['Location'])

    def test_template(self):
        response = self.client.get('')
        self.assertContains(response, "Список товаров")

    def test_login_required(self):
        user = User.objects.create_user(username='alex', password='123')
        self.client.force_login(user)
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)

    def test_anonymous_login(self):
        self.product = Product.objects.create(name='Laptop', price=500)
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, 403)
