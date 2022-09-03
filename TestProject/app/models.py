from django.db import models


class Product(models.Model):
    table_name = 'product'
    # fields: № id is created by default
    # заказ №
    # стоимость,$
    # срок поставки,
    # стоимость в руб.
    id = models.IntegerField(primary_key=True, unique=True)
    order_number = models.IntegerField()
    cost = models.FloatField()
    delivery_time = models.DateField()
    cost_in_rub = models.FloatField()

