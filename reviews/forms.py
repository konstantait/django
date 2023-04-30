from django import forms
from django.utils.html import strip_tags

from reviews.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('author', 'product', 'rating', 'text')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].widget = forms.HiddenInput()
        self.fields['author'].initial = user

    def clean_text(self):
        data = strip_tags(self.cleaned_data['text'])
        if not data:
            raise forms.ValidationError('Text field empty after clearing html-tags') # noqa
        return data
