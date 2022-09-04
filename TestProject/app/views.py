from django.shortcuts import render
from .models import Product, Overdue

def index(request):
    # get all products from the database sorted by delivery_time
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})
