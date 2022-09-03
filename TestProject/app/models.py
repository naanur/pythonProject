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


class Overdue(models.Model):
    # просроченные заказы хранятся в отдельной таблице
    # потому что таблица product каждый раз очищается и заполняется заново
    order_number = models.IntegerField()
    message_sent = models.BooleanField()
