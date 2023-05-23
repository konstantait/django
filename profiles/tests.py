from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

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
