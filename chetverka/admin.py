from django.contrib import admin
from chetverka.models import bankCard, Transaction, Ticket, PricesAndProducts, logger

@admin.register(bankCard)
class bankCardSupervisor(admin.ModelAdmin):
    list_display = ('id', 'card_value', 'expired_month', 'expired_year', 'card_holder', 'telegramuser')

@admin.register(Transaction)
class TransactionSupervisor(admin.ModelAdmin):
    list_display = ('id', 'tr_datetime', 'tr_status', 'bankcard')

@admin.register(Ticket)
class TicketSupervisor(admin.ModelAdmin):
    list_display = ('id', 'ticket_number', 'transaction', 'tovar')

@admin.register(PricesAndProducts)
class PricesAndTicketSupervisor(admin.ModelAdmin):
    list_display = ('id', 'price', 'product', 'service')

@admin.register(logger)
class logger(admin.ModelAdmin):
    list_display = ('id', 'dt', 'log', 'error')