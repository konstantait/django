import re
from bs4 import BeautifulSoup

from catalog.api_client import APIBaseClient


class DevConstantaUA(APIBaseClient):
    base_url = 'https://dev.constanta.ua/ru'

    __categories = {}
    # noqa https://dev.constanta.ua/ru/80-divany -> https://dev.constanta.ua/ru/80-divany?id_category=80&n=122 # noqa
    # noqa https://dev.constanta.ua/ru/56-kresla-i-pufy -> https://dev.constanta.ua/ru/56-kresla-i-pufy?id_category=56&n=26
    # noqa {
    # noqa '80-divany': {'children': ['80-pryamye-divany', '80-uglovye-divany', '80-divany-akkordeon'],
    # noqa                    'count': '122', 'url': 'https://dev.constanta.ua/ru/80-divany'},
    # noqa '56-kresla-i-pufy': {'children': [], 'count': '26', 'url': 'https://dev.constanta.ua/ru/56-kresla-i-pufy'},
    # noqa '55-krovati': {'children': [], 'count': '15', 'url': 'https://dev.constanta.ua/ru/55-krovati'},
    # noqa '54-korpusnaya-mebel': {'children': ['54-kukhonnye-garnitury', '54-shkafy-kupe-ergosens', '54-shkafy-kupe', '54-stoly', '54-spalnya-zlata'],
    # noqa                    'count': '54', 'url': 'https://dev.constanta.ua/ru/54-korpusnaya-mebel'},
    # noqa '82-kukhonnaya-mebel': {'children': ['82-kukhonnye-garnitury', '82-kukhonnye-stulya', '82-uglovye-divany'],
    # noqa                    'count': '18', 'url': 'https://dev.constanta.ua/ru/82-kukhonnaya-mebel'},
    # noqa '58-aksessuary': {'children': ['58-stoly'], 'count': '22', 'url': 'https://dev.constanta.ua/ru/58-aksessuary'},
    # '57-akcii': {'children': ['57-shkafy-kupe-ergosens'], 'count': '15', 'url': 'https://dev.constanta.ua/ru/57-akcii'}}

    __products = {}
    # {
    # '413-rolf': {'category': '80-pryamye-divany', 'model': 'Прямой диван Рольф', 'price': 19200, 'price_old': 25600,
    #                'image': 'https://dev.constanta.ua/5883-tm_home_default/rolf.jpg'},
    # '451-rosetta': {'category': '80-uglovye-divany', 'model': 'Угловой диван Розетта', 'price': 0, 'price_old': 0,
    #                'image': 'https://dev.constanta.ua/5641-tm_home_default/rosetta.jpg'},
    # }

    def parse(self) -> tuple:
        self.update_top_level_categories()
        # Update the amount of products in the top level categories
        for _, item in self.__categories.items():
            item['count'] = self.get_products_count(item['url'])
        for key, item in self.__categories.items():
            # https://dev.constanta.ua/ru/80-divany?id_category=80&n=122
            url = f"{item['url']}?id_category={key.split('-', 1)[0]}&n={item['count']}"
            self.get_products(url, key)
        return self.__categories, self.__products

    def update_top_level_categories(self):
        self._request('get', self.base_url)
        if self.response and self.response.status_code == 200:
            soup = BeautifulSoup(self.response.content, 'html.parser')
            for item in soup.find_all('a', class_=re.compile('top-level-menu-li-a tmmegamenu_item')):  # noqa
                # https://dev.constanta.ua/ru/80-divany'
                href = item.get('href')
                slug = href.split('/')[-1]
                if slug:
                    self.__categories[slug] = {'children': [], 'count': 0, 'url': href} # noqa

    def get_products_count(self, url):
        self._request('get', url)
        count = 0
        if self.response and self.response.status_code == 200:
            soup = BeautifulSoup(self.response.content, 'html.parser')
            # Показано 1 - 15 из 122 товаров
            count = re.findall(r'\d+', list(soup.find('div', class_='product-count').stripped_strings)[0])[-1] # noqa
        return count

    def get_products(self, url, parent):
        self._request('get', url)
        if self.response and self.response.status_code == 200:
            soup = BeautifulSoup(self.response.content, 'html.parser')
            parent_category_id = parent.split('-', 1)[0]
            parent_category_name = parent.split('-', 1)[1]
            for item in soup.find_all('div', class_='product-container'):
                product = item.find('a', class_='product_img_link')
                href = product.get('href')
                title = product.get('title')
                image = product.img.get('src')

                price_old = item.find('span', class_='old-price product-price') # noqa
                if price_old:
                    price_old = int(''.join(re.findall(r'\d+', price_old.string)))
                else:
                    price_old = 0

                if price_old == 0:
                    price_new = item.find('span', class_='price product-price')  # noqa
                else:
                    price_new = item.find('span', class_='price product-price product-price-new')

                if price_new:
                    price_new = int(''.join(re.findall(r'\d+', price_new.string)))
                else:
                    price_new = 0

                # parent url https://dev.constanta.ua/ru/80-divany?id_category=80&n=122
                # -> https://dev.constanta.ua/ru/pryamye-divany/39-orion.html
                # pryamye-divany != divany -> 80-pryamye-divany, sort = 2
                category = href.split('/')[-2]
                if category != parent_category_name:
                    category = f"{parent_category_id}-{category}"
                    children = self.__categories[parent]['children']
                    if category not in children:
                        children.append(category)
                else:
                    category = parent

                # https://dev.constanta.ua/ru/pryamye-divany/39-orion.html
                slug = href.split('/')[-1].replace('.html', '')
                if slug:
                    self.__products[slug] = {
                        'category': category,
                        'name': title,
                        'price': price_new,
                        'price_old': price_old,
                        'image': image
                    }

    def get_image(self, url):
        self._request('get', url=url)
        return self.response


dev_constanta_ua = DevConstantaUA()
