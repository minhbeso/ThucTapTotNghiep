from django import forms
from .models import Order


class OrderPaymentPrepareForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "payment_method",
            "message",
            "address",
            "total_payment",
        ]
