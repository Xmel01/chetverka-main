var counter = 0; // счетчик общего количества добавленных продуктов
$(document).ready(function(){
    $('.badge').text(counter); // устанавливает счетчик добавленных продуктов при загрузке страницы

});

var csrftoken = $.cookie('csrftoken'); // csrf токен

function addElement(){ // функция добавления элементов в форму оплаты
    var all_counters = $("div[id^='counter']"); // выбираем все счетчики товаров
    var total_sum = 0; // инициализируем переменную итоговой суммы
    for (var i=0; i<all_counters.length;i++){ // перебираем все счетчики
        let value = parseInt($(all_counters[i]).text()); // берем выбранное количество из перебранного счетчика
        let price = parseInt($(all_counters[i]).parents(2).children('.cardTitle').text().match(/\d{3,4}/)); // ищем в счетчике цифры от 3 до 4 символов
        let mul = value * price; // умножаем количество на сумму
        total_sum += mul;
    }
    $('#total').text('Всего на сумму: ' + total_sum +' ₽'); // выводим полученную сумму во вьюпорт
    return total_sum; // возвращаем значение, чтобы потом его использовать
}


$(document).on('click', '[id^=cell-btn]', function() { // собитие при нажании на кнопку Добавить
    counter++; // увеличиваем общий счетчик на 1
    let button_id = ($(this).attr('id')).split(' ')[1]; // получаем id нажатой кнопки "добавить"
    let card = $(this).parents(1).children('.cardTitle').text(); // даем значению card название карточки
    $(this).parent().html('<div class="row"><button class="btn btn-outline-success col-sm-4" id="plus ' + button_id +'"><span>+</span></button><button onclick="addElement()" class="btn btn-outline-danger col-sm-4" id="minus ' + button_id +'"><span>-</span></button><div class="alert-primary col-sm-4" id="counter'+ button_id + '">1</div></div>');
    $('div[rel=item-container]').prepend('<div class="alert alert-success" id="basket-item '+ button_id + '">1 ' + card + '</div>');
    $('.badge').text(counter);
    addElement();
    $('#body').append('<button class="btn-success rounded-top" onclick="payFunction()" id="payment">Оплатить</button>')
})

function payFunction(){
    let prods = $('div[rel=item-container]').children();
    for (let p=0;p<prods.length;p++){
       $('#modal-body').append(prods[p]);
           }
    $('#modal').modal('show');
}


function proceed(){
    let need_array = $('#modal-body').children('[id^=basket-item]');
    let spisok = [];
    for (let s=0;s<need_array.length;s++){
            let items = $(need_array[s]).text();
            spisok.push(items);
        }
    let data = addElement();
    let bankCard = []
    bankCard.push(JSON.stringify($('#owner').val()))
    bankCard.push(JSON.stringify($('#cvv').val()))
    bankCard.push(JSON.stringify($('#cardNumber').val()))
    bankCard.push(JSON.stringify($('#selectMonth option:selected').text()))
    bankCard.push(JSON.stringify($('#selectYear option:selected').text()))

    $.ajax({
            url: "payform/",
            method: "post",
            //dataType: 'json',

            headers: {
              'X-CSRFToken': csrftoken
            },
            async: false,
            data: {
                'data': data,
                'description': spisok,
                'bank_card': bankCard,
            },
            success: function() {
                alert('done');

            }
        })
    //window.location.reload()
}

$(document).on('click', '[id^=plus]', function(){
    counter++;
    let plus_id = ($(this).attr('id')).split(' ')[1];
    let count = parseInt($(this).siblings('.alert-primary').text()); // берем количество товара на карточке и переводим в Integer
    $(this).siblings('.alert-primary').text(count+1); // Прибавляем число
    let all_baskets = $('[rel="item-container"]').children();
    for (var i = 0; i < all_baskets.length; i++) {
        let basket = $(all_baskets[i]);
        if ('basket-item '+ plus_id === basket.attr('id')) {
           let string = basket.text().split(' ')[0];
           let container = basket.text().replace(string, count+1);
           basket.text(container);
           addElement();
           }
    }

     $('.badge').text(counter);// Кол-во товаров всего (иконка рядом с корзиной)
});

$(document).on('click', '[id^=minus]', function(){
    counter--;
    $('.badge').text(counter);
    let plus_id = ($(this).attr('id')).split(' ')[1];
    let count = parseInt($(this).siblings('.alert-primary').text()); // берем количество товара на карточке и переводим в Integer
    $(this).siblings('.alert-primary').text(count-1); // Прибавляем число
    let all_baskets = $('[rel="item-container"]').children();
    for (var i = 0; i < all_baskets.length; i++) {
        let basket = $(all_baskets[i]);
        if ('basket-item '+ plus_id === basket.attr('id')) {
           let string = basket.text().split(' ')[0];
           let container = basket.text().replace(string, count-1);
           if (count === 1){
               basket.remove();
           }
           else{
               basket.text(container);
           }
        }
    }
});

