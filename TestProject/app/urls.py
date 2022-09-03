from django.urls import path, include
from . import views
from rest_framework import routers, serializers, viewsets
from .models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'order_number', 'cost', 'delivery_time', 'cost_in_rub']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
]
