from decimal import Decimal
from django.conf import settings
from shop.myshop.models import Product


class Cart(object):

    def __init__(self, request):
        """Инициализация корзины(готовность к использованию)
        передаем запрос(request),self.session запоминает текущую сессию
        get получает данные
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Если нет товара в корзине,то сохраняем ПУСТУЮ КОРЗИНУ В СЕССИИ и возвращаем ее
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Перебираем товары в корзине и получаем товары из базы данных.
        создаем копию объекта корзины,для каждого товара преобразуем
        цену из строки в число с фиксированной точностью
        вычисляем стоимость с учетом цены количества

        """
        product_ids = self.cart.keys()
        # Получаем товары и добавляем их в корзину
        products = Product.objects.filter(id_in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Считаем сколько товаров в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавляем товар в корзину или обновляем его количество
        quantity- не обязательное количество ,по умолчанию 1,
        update_quantity-нужно заменить кол-во товаров на новые или добавить существующие
        если товара в корзине нет,то добавляем,если есть то плюсуем кол-во,
        сохраняем
         """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """сохраняем товар"""
        self.session.modified = True

    def remove(self, product):
        """Удаляем товар"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        # получаем общую стоимость =цена * на кол-во
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # очищаем корзину в сессии

        del self.session[settings.CART_SESSION_ID]
        self.save()
