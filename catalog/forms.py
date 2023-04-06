from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

from catalog.models import Review


class ReviewModelForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('author', 'product', 'rating', 'text')

    def __init__(self, author, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].widget = forms.HiddenInput()
        self.fields['author'].initial = author

    def clean_text(self):
        data = strip_tags(self.cleaned_data['text'])
        if not data:
            raise ValidationError("Text field empty after clearing html-tags")
        return data
