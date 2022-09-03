from django.db import models


class Product(models.Model):
    # fields: № id is created by default
    # заказ №
    # стоимость,$
    # срок поставки,
    # стоимость в руб.
    order_number = models.IntegerField()
    cost = models.FloatField()
    delivery_time = models.DateField()
    cost_in_rub = models.FloatField()

