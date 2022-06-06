from django.db import models
from teletroyka.models import TelegramUser


class bankCard(models.Model):
    card_value = models.CharField('Номер карты', max_length=16)
    expired_month = models.CharField('Месяц истечения', max_length=2)
    expired_year = models.CharField('Год истечения', max_length=2)
    card_holder = models.CharField('Владелец карты', max_length=30)
    telegramuser = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, blank=True, null=True, )

    def __str__(self):
        return f'{self.id} '

    class Meta:
        verbose_name = 'Банковская карта'
        verbose_name_plural = 'Банковские карты'

class Transaction(models.Model):
    tr_datetime = models.DateTimeField('Дата и время транзакции', auto_now=True)
    tr_status = models.CharField('Статус транзакции', max_length=10)
    tr_obj_description = models.CharField('Описание покупки', max_length=500)

    bankcard = models.ForeignKey('bankCard', on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return f'{self.id} '

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

class Ticket(models.Model):
    ticket_type = models.CharField('Название билета', max_length=15)
    ticket_number = models.CharField('Номер билета', max_length=10, unique=True)
    ticket_datetime = models.DateTimeField('Дата и время отправления', auto_now=False)

    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.id} '

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'


class PricesAndProducts(models.Model):
    price = models.CharField('Цена', max_length=6)
    product = models.CharField('Товар', max_length=50)
    service = models.CharField('Описание товара', max_length=100)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.id} ' + f'{self.price} ' + f'{self.product} ' + f'{self. service}'

    class Meta:
        verbose_name = 'Цена и продукт'
        verbose_name_plural = 'Цены и продукты'
