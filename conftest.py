import faker
import pytest

import factory.django
from pytest_factoryboy import register
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from core.constants import DECIMAL_PLACES
from core.settings import SECRET_KEY
from catalog.models import Category, Product
from currencies.models import Currency
from reviews.models import Review

fake = faker.Faker()


@pytest.fixture(scope='session')
def faker_fixture():
    yield fake


@pytest.fixture(autouse=True)
def django_db_setup(db):
    Currency.objects.create(code='USD', rate=1)
    Currency.objects.create(code='EUR', rate=0.9)
    Currency.objects.create(code='UAH', rate=37)
    yield


@register
class UserFactory(factory.django.DjangoModelFactory):
    email = factory.LazyAttribute(lambda x: fake.email())
    phone = factory.LazyAttribute(lambda x: fake.phone_number()) # noqa
    is_phone_valid = True

    class Meta:
        model = get_user_model()
        django_get_or_create = ('email', )


@pytest.fixture(scope='function')
def login_client(db, client):
    def login_user(user=None, **kwargs):
        if user is None:
            user = UserFactory()
        user.set_password(SECRET_KEY)
        user.save()
        data = {
            'username': user.email,
            'password': SECRET_KEY
        }
        response = client.post(reverse_lazy('profiles:login'), data=data)
        assert response.status_code == 302
        return client, user
    return login_user


@register
class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(lambda x: fake.word())
    slug = factory.LazyAttribute(lambda x: fake.word())

    class Meta:
        model = Category
        django_get_or_create = ('slug', )


@register
class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(lambda x: fake.word())
    slug = factory.LazyAttribute(lambda x: fake.word())
    sku = factory.LazyAttribute(lambda x: fake.word())
    price = factory.LazyAttribute(lambda x: fake.pydecimal(min_value=0, left_digits=4, right_digits=DECIMAL_PLACES)) # noqa

    class Meta:
        model = Product
        django_get_or_create = ('slug', )

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)


@register
class ReviewFactory(factory.django.DjangoModelFactory):
    author = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    text = factory.LazyAttribute(lambda x: fake.text())

    class Meta:
        model = Review
