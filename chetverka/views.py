from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from chetverka.models import Ticket, PricesAndProducts, Transaction, bankCard, logger
from django.views.generic import DetailView
from chetverka.forms import bankCardForm
from teletroyka.models import TelegramUser
import re, random, json

from rest_framework.parsers import JSONParser


def log(request):
    search_query = request.GET.get('search')
    data = Ticket.objects.all()
    if search_query == None:
        data = Ticket.objects.filter(id__in=data).order_by('id')
    elif re.match(r"\D{2,}", search_query) != None:
        data = Ticket.objects.filter(id__in=data, ticket_type__contains=search_query).order_by('-id')
    elif re.match(r"\d{10}", search_query) != None:
        data = Ticket.objects.filter(id__in=data, ticket_number__contains=search_query).order_by('-id')
    elif re.search(r"\d{1,}", search_query) != None:
        data = Ticket.objects.filter(id__in=data, id__contains=search_query).order_by('-id')
    else :
        print('Not Found')
    return render(request, 'chetverka/log.html', {'Ticket': data})


class Detalization(DetailView):
    model = Ticket
    template_name = 'chetverka/detalization.html'
    context_object_name = 'record'


def base(request):
    data = PricesAndProducts.objects.all()
    return render(request, 'chetverka/base.html', {'price': data})

class PricesAndProductsController(DetailView):
    model = PricesAndProducts
    template_name = 'base/chetverka/payform.html'
    context_object_name = 'record'
    form = bankCardForm



    def get_context_data(self, **kwargs):

        context = super(PricesAndProductsController, self).get_context_data(**kwargs)
        context['form'] = bankCardForm()
        return context

    def post(self, request, *args, **kwargs):
        user = TelegramUser.objects.get(pk=1) #ID юзера изменить!!
        if request.method == 'POST':
            form = bankCardForm(request.POST)
            if form.is_valid():
                bank_card = form.save(commit=False)
                print(bank_card)
                bank_card.telegramuser = user
                print(bank_card)
                bank_card.save()
                transact = Transaction.objects.create(tr_status='Succeed', bankcard=bank_card)
                Ticket.objects.create(ticket_type='Тройка', ticket_number=random.randint(1000000000, 9999999999), transaction=transact)
                return render(request, 'chetverka/status.html')
        else:
            form = bankCardForm(initial=user)

        return render(request, 'chetverka/base.html', {'form': form})

def test(request):
    return render(request, 'chetverka/TestView.html')

@api_view(['POST'])
def pay(request):

    print(request.data)
    data = dict(request.data)

    data1 = str(data.get('description[]'))
    user_id = re.search(r"\d{9,10}", str(data.get('tg_user_data')))

    try:
        teleuser = TelegramUser.objects.get(telegram_user_id=user_id[0])
        bank_card = bankCard.objects.create(card_value=data.get('bank_card[]')[2], expired_month=data.get('bank_card[]')[3], expired_year=data.get('bank_card[]')[4], card_holder=data.get('bank_card[]')[0], telegramuser=teleuser)
        transact = Transaction.objects.create(tr_status='Succeed', tr_obj_description=data.get('description[]'), bankcard=bank_card)

        match = re.findall(r"'\d{1,2}", data1)
        match1 = re.findall(r"\d{1,2}", str(match))
        name = re.findall(r"Билет \w* \"\D*\"", data1)
        print(len(data['description[]']))

        for i in range(len(data['description[]'])):
            prod = PricesAndProducts.objects.get(product=name[i])
            for a in range(int(match1[i])):
                Ticket.objects.create(ticket_number=random.randint(1000000000, 9999999999), transaction=transact, tovar=prod)
        logger.objects.create(log=request.data, error=None)
    except Exception as e:
        logger.objects.create(log=user_id, error=e)


    return Response({'status': 1})