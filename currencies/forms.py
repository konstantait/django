from django import forms


class CurrencySelectForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currencies'] = forms.ChoiceField(
            choices=((1, 'UAH'), (2, 'USD'), (3, 'EUR')),
            widget=forms.Select(attrs={'onchange': 'submit();'})
        )
