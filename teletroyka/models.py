from django.db import models

class TelegramUser(models.Model):
    telegram_user_id = models.CharField('Telegram ID пользователя', max_length=9)
    telegram_user_first_name = models.CharField('Имя пользователя', max_length=15)
    telegram_user_last_name = models.CharField('Фамилия пользователя',max_length=15)
    telegram_user_nickname = models.CharField('Никнейм пользователя', max_length=30)

    def __str__(self):
        return f'{self.telegram_user_first_name} ' + f'{self.telegram_user_nickname}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'