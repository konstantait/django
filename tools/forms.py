import csv
import decimal
from io import StringIO

from django import forms
from django.core.validators import FileExtensionValidator

from core.constants import (
    CSV_FIELDS_DELIMITER,
    CSV_IN_FIELD_DELIMITER,
    # CSV_IN_FIELD_ATTR_DELIMITER,
)
from catalog.models import (
    # AttributeGroup,
    # Attribute,
    Category,
    Product,
)


class UploadCSVForm(forms.Form):
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
            categories = []
            if row['categories']:
                categories_names = row['categories'].split(CSV_IN_FIELD_DELIMITER) # noqa
                for name in categories_names:
                    category, _ = Category.objects.get_or_create(name=name)
                    categories.append(category)
            # attributes = []
            # if row['attributes']:
            #     attributes_names = row['attributes'].split(CSV_IN_FIELD_DELIMITER) # noqa
            #     for name in attributes_names:
            #         attribute_group_name, attribute_name = \
            #             name.split(CSV_IN_FIELD_ATTR_DELIMITER)
            #         attribute_group, attribute_group_created = \
            #             AttributeGroup.objects.get_or_create(name=attribute_group_name)  # noqa
            #         if attribute_group_created:
            #             attribute = Attribute(
            #                 attribute_group=attribute_group,
            #                 name=attribute_name
            #             )
            #             attribute.save(force_insert=True)
            #         else:
            #             attribute = Attribute.objects.get(
            #                 attribute_group=attribute_group,
            #                 name=attribute_name
            #             )
            #         attributes.append(attribute)

            if row['sku']:
                try:
                    _ = Product(
                        sku=row['sku'],
                        name=row['name'],
                        model=row['model'],
                        description=row['description'],
                        price=decimal.Decimal(row['price']),
                    )
                    product, _ = Product.objects.update_or_create(sku=row['sku']) # noqa
                    product.name = row['name']
                    product.model = row['model']
                    product.description = row['description']
                    product.price = decimal.Decimal(row['price'])
                    product.categories.clear()
                    product.categories.set(categories)
                    # product.attributes.clear()
                    # product.attributes.set(attributes)
                    product.save()
                except (KeyError, decimal.InvalidOperation) as err:
                    # logging, continuing work
                    print(f'Error {err}')
