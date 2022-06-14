from django.contrib import admin
from teletroyka.models import TelegramUser

@admin.register(TelegramUser)
class TelegramUserSupervisor(admin.ModelAdmin):
    list_display = ('id', 'telegram_user_id', 'telegram_user_first_name', 'telegram_user_last_name', 'telegram_user_nickname')