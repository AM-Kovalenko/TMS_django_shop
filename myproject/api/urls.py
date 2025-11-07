from django.urls import path

from api.views import test_api, ProductDetailAPIView, ProductListAPIView, ProductCreateAPIView, set_cookie_example, get_cookie_example


urlpatterns = [
    path('test/', test_api),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/create/', ProductCreateAPIView.as_view(), name='product-create'),

    path('set-cookie/', set_cookie_example),
    path('get-cookie/', get_cookie_example),
]