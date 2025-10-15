from django.urls import path

from .views import HelloWorldView, products_view, product_detail, ProductCreateView

urlpatterns = [
    path('hello/', HelloWorldView.as_view()),
    path('products/', products_view, name='products'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    # path('product/create/', create_product, name='create_product'),
    path('product/create/', ProductCreateView.as_view(), name='create_product'),
]
