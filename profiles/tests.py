from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from phonenumber_field.phonenumber import PhoneNumber

from profiles.utils import store_key_hash_in_session, verify_key_hash_from_session, verify_key, hash_key  # noqa

User = get_user_model()


def test_login(client, faker, login_client):
    url = reverse_lazy('profiles:login')
    response = client.get(url)
    assert response.status_code == 200

    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert all(v == ['This field is required.']
               for v in response.context['form'].errors.values())

    data['username'] = faker.email()
    data['password'] = faker.word()
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'] == [
        'Please enter a correct email address and password. Note that both fields may be case-sensitive.'] # noqa

    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200


def test_signup(client, faker, user_factory):
    url = reverse_lazy('profiles:signup')
    response = client.get(url)
    assert response.status_code == 200

    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert all(v == ['This field is required.']
               for v in response.context['form'].errors.values())

    user = user_factory()
    password = faker.word()
    data = {
        'email': user.email,
        'password1': password,
        'password2': faker.word()
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    errors = response.context['form'].errors
    assert errors['email'] == ['User with that email already exists']
    assert errors['password2'] == ['The two password fields didn’t match.']

    data['email'] = faker.email()
    data['password2'] = password
    response = client.post(url, data=data)
    assert response.status_code == 200
    errors = response.context['form'].errors
    assert errors['password2'] == [
        'This password is too short. It must contain at least 8 characters.']

    password = faker.password()
    data['password1'] = password
    data['password2'] = password
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse_lazy('profiles:login')
    assert response.redirect_chain[0][1] == 302


def test_update(faker, login_client):
    client, user = login_client()
    kwargs = {
        'pk': f'{user.id}'
    }
    url = reverse_lazy('profiles:update', kwargs=kwargs)
    response = client.get(url)
    assert response.status_code == 200
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': PhoneNumber.from_string(f'+38050{faker.random_number(digits=7)}') # noqa
    }

    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse_lazy('profiles:verification') # noqa
    assert response.redirect_chain[0][1] == 302


def test_verification(client, faker):
    phone = PhoneNumber.from_string(f'+38050{faker.random_number(digits=7)}')  # noqa
    secret_key = str(faker.random_number(digits=10))
    url = reverse_lazy('profiles:verification')
    response = client.get(url)
    session = client.session
    assert response.status_code == 200
    assert store_key_hash_in_session(session, phone, secret_key) == phone
    assert verify_key_hash_from_session(session, secret_key) == phone

    data = {'secret_key': ''}
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200

    data = {'secret_key': secret_key}
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse_lazy('profiles:logout')
    assert response.redirect_chain[0][1] == 302
