import csv
import decimal
from io import StringIO

from django import forms
from django.utils.html import strip_tags
# from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from core.constants import (
    CSV_FIELDS_DELIMITER,
    CSV_IN_FIELD_DELIMITER,
    CSV_IN_FIELD_ATTR_DELIMITER
)
from catalog.models import (
    AttributeGroup,
    Attribute,
    Category,
    Product,
    Review,
)


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


class ImportCSVForm(forms.Form):
    file = forms.FileField(
        validators=[FileExtensionValidator(['csv'])]
    )

    def save(self):
        csv_file = self.cleaned_data['file']
        reader = csv.DictReader(StringIO(
            csv_file.read().decode('utf-8')),
            delimiter=CSV_FIELDS_DELIMITER
        )
        for row in reader:
            product, product_created = Product.objects.get_or_create(
                name=row['name'],
                model=row['model'],
                sku=row['sku'],
                description=row['description'],
                price=decimal.Decimal(row['price']),
            )

            categories = []
            product.categories.clear()
            print('product.categories.clear()')
            categories_names = row['categories'].split(CSV_IN_FIELD_DELIMITER)
            for name in categories_names:
                category, _ = Category.objects.get_or_create(name=name)
                categories.append(category)
            product.categories.set(categories)
            print('product.categories.set()')

            attributes = []
            product.attributes.clear()
            print('product.attributes.clear()')
            attributes_names = row['attributes'].split(CSV_IN_FIELD_DELIMITER)
            for name in attributes_names:
                attribute_group_name, attribute_name = \
                    name.split(CSV_IN_FIELD_ATTR_DELIMITER)
                attribute_group, attribute_group_created = \
                    AttributeGroup.objects.get_or_create(name=attribute_group_name) # noqa
                if attribute_group_created:
                    attribute = Attribute(
                        attribute_group=attribute_group,
                        name=attribute_name
                    )
                    attribute.save(force_insert=True)
                else:
                    attribute = Attribute.objects.get(
                        attribute_group=attribute_group,
                        name=attribute_name
                    )
                attributes.append(attribute)
            product.attributes.set(attributes)
            print('product.attributes.set()')

            product.save()
