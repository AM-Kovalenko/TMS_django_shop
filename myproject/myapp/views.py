from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import ProductForm
from .models import Product


class HelloWorldView(View):
    def get(self, request):
        return HttpResponse("Hello, World!",)


def products_view(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

# def create_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()  # сохраняем новый объект в БД
#             return redirect('products')  # можно переадресовать на любую страницу
#     else:
#         form = ProductForm()
#
#     return render(request, 'create_product.html', {'form': form})

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = reverse_lazy('products')
