from pprint import pprint

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from myapp.models import Product
from rest_framework.views import APIView

from api.serializers import ProductSerializer, RegisterSerializer, ProductDiscountSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsManager, IsClient
import logging

logger = logging.getLogger("api")


@api_view(['GET'])
def test_api(request):
    products = Product.objects.all()
    category = request.query_params.get('category')
    if category:
        products = products.filter(category_id=category)
    data = [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price,
        } for product in products
    ]
    return Response(data)


class ProductDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Каждый может посмотреть товар.

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
        return Response({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'price_with_vat': product.price_with_vat
        })


class ProductListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Список продуктов",
        operation_description="Получение списка продуктов с фильтрацией",
        responses={
            200: ProductSerializer(many=True)
        },
    )
    # @method_decorator(cache_page(30))
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsManager]

    @swagger_auto_schema(
        operation_summary="Создать продукт",
        operation_description="Создание нового товара. Требуются права менеджера.",
        request_body=ProductSerializer,
        responses={
            201: """ some text .
            
            {
                "id": 285,
                "name": "string",
                "description": "string",
                "price": "123.00",
                "in_stock": true,
                "category": 1,
                "image": null
            }""",

            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden'
        },
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)  # десериализация входных данных
        if serializer.is_valid():  # проверка данных
            serializer.save()  # создание нового объекта Product
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        pprint(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def set_cookie_example(request):
    response = Response({'message': 'Cookie установлено'})
    response.set_cookie(
        key='user_token',
        value='12345abcdef',
        max_age=15,  # 1 час
        httponly=True  # запрещает доступ к cookie из JS
    )
    return response


@api_view(['GET'])
def get_cookie_example(request):
    token = request.COOKIES.get('user_token')
    if token:
        return Response({'message': 'Cookie найден', 'token': token})
    return Response({'message': 'Cookie не найден'}, status=404)


class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # регистрация открыта

    @swagger_auto_schema(
        operation_summary="Регистрация пользователя",
        operation_description="Создание нового аккаунта. Пароль должен быть не менее 8 символов.",
        request_body=RegisterSerializer,
        responses={
            201: """{
                "id": 6,
                "username": "client",
                "email": "user@example.com"
            }""",
            400: "Ошибки валидации данных"
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            # помечаем refresh в blacklist
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Token invalid or already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)


class SetDiscountAPIView(APIView):
    permission_classes = [IsAuthenticated, IsClient]

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)

        serializer = ProductDiscountSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Discount updated",
                "product_id": product.id,
                "discount_percent": product.discount_percent
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
