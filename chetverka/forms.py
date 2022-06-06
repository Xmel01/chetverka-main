from django.forms import ModelForm, TextInput, HiddenInput
from chetverka.models import bankCard
from teletroyka.models import TelegramUser


class bankCardForm(ModelForm):
    class Meta:
        model = bankCard
        fields = ['card_value', 'expired_month', 'expired_year', 'card_holder', 'telegramuser']
        widgets = {
            'card_value': TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер карты'}),
            'expired_month': TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите месяц истечения'}),
            'expired_year': TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите год истечения'}),
            'card_holder': TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя держателя карты'}),
            'telegramuser': HiddenInput(attrs={'class': 'form-control'})
        }

