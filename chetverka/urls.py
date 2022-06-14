from django.urls import path
from . import views

urlpatterns=[
    path('log/', views.log, name="log"),
    path('chetverka/detalization/<int:pk>', views.Detalization.as_view(), name="details"),
    #path('base/chetverka/payform/<int:total_sum>', views.PricesAndProductsController.as_view(), name="pricesandproducts"),
    path('base/', views.base, name='base'),
    path('test/', views.test, name='test'),
    path('base/payform/', views.pay, name='pay')
]

