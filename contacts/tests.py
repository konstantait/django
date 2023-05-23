from django.urls import reverse_lazy


def test_contacts_send(client, faker):
    url = reverse_lazy('contacts:send')
    response = client.get(url)
    assert response.status_code == 200

    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert all(v == ['This field is required.'] for v in response.context['form'].errors.values()) # noqa

    data['email'] = 'faker.email()'
    data['text'] = faker.word()
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['email'] == ['Enter a valid email address.']  # noqa

    data['email'] = faker.email()
    data['text'] = faker.word()
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse_lazy('catalog:home')
    assert response.redirect_chain[0][1] == 302
