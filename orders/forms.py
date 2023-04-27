from django import forms
from .models import Order, Coupon


class OrderCreateForm(forms.ModelForm):
    coupon = forms.CharField()

    class Meta:
        model = Order
        fields = ['name', 'email', 'phone']

    def save(self, commit=True):
        order = super().save(commit=False)
        order.coupon = Coupon.objects.filter(code=self.cleaned_data['coupon']).first() # noqa
        if commit:
            order.save()
        return order
