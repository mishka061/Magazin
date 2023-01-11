from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),# Адрес корзины полностью
    path('add/<int:product_id>/',
         views.cart_add,
         name='cart_add'),# Добавление корзины
    path('remove/<int:product_id>/',
         views.cart_remove,
         name='cart_remove'),# Удаление корзины
]
