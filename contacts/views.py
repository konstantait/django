from django.urls import reverse_lazy
from django.views.generic import FormView

from contacts.forms import ContactForm
from contacts.tasks import send_contact_message


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'contacts/send.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        send_contact_message.delay(
            [form.cleaned_data["email"], ],
            form.cleaned_data["text"]
        )
        return super().form_valid(form)
