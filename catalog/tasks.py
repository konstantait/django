from io import BytesIO
import logging

from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from django.core.validators import URLValidator

from core.enums import StatusTypes
from catalog.clients.constanta import dev_constanta_ua
from catalog.models import Product, Category
from core.celery import app

logger = logging.getLogger(__name__)

# categories_dict = {
# '80-divany': {'children': ['80-pryamye-divany', '80-uglovye-divany', '80-divany-akkordeon'],
#                    'count': '122', 'url': 'https://dev.constanta.ua/ru/80-divany'},
# '56-kresla-i-pufy': {'children': [], 'count': '26', 'url': 'https://dev.constanta.ua/ru/56-kresla-i-pufy'},
# }
# products_dict = {
# '413-rolf': {'category': '80-pryamye-divany', 'model': 'Прямой диван Рольф', 'price': 19200, 'price_old': 25600,
#                'image': 'https://dev.constanta.ua/5883-tm_home_default/rolf.jpg'},
# '451-rosetta': {'category': '80-uglovye-divany', 'model': 'Угловой диван Розетта', 'price': 0, 'price_old': 0,
#                'image': 'https://dev.constanta.ua/5641-tm_home_default/rosetta.jpg'},
# }


@app.task
def parse_products():
    categories_dict, products_dict = dev_constanta_ua.parse()
    save_parser_result.delay(categories_dict, products_dict)


@app.task
def save_parser_result(categories: dict, products: dict):
    for top_category, value in categories.items():
        defaults = {
            'name': top_category,
            'sort_order': 0,
            'status': StatusTypes.DISABLED

        }
        parent_category, create = Category.objects.get_or_create(slug=top_category, defaults=defaults) # noqa
        if create:
            for slug in value['children']:
                defaults = {
                    'name': slug,
                    'parent': parent_category,
                    'sort_order': 0,
                    'status': StatusTypes.DISABLED

                }
                Category.objects.get_or_create(slug=slug, defaults=defaults)

    for slug, value in products.items():
        sku = value['category'].split('-', 1)[0]
        sku = f"{sku}-{slug.split('-', 1)[0]}"
        defaults = {
            'name': value['name'],
            'sku': sku,
            'price': value['price'],
        }
        product, _ = Product.objects.update_or_create(slug=slug, defaults=defaults)
        product.categories.add(Category.objects.get(slug=value['category']))

        image = value['image']
        validate_url = URLValidator()
        try:
            validate_url(image)
        except ValidationError:
            logger.error('not found', image)
        else:
            logger.info(image)
            image_data = dev_constanta_ua.get_image(image)
            image = ImageFile(BytesIO(image_data.content), name=image)
            product.image = image
            product.save(update_fields=('image',))
