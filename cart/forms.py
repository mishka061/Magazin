from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 20)]


# Количество выбранного товара для добавления

class CartAddProductForm(forms.Form):
    """
    Обработчик для удаления,обновления,добавления корзины
    """
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int
    )  # количество товара,которое преобразовывается в инт
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )  # обновлять или заменять количество единиц товара
