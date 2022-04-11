from django.shortcuts import render, redirect
from django.contrib.messages import success
from django.views.generic import View

from .forms import ContactForm

class ContactView(View):
    form_class = ContactForm
    template_name = 'contact.html'

    def get(self, request):
        return render(
            request,
            self.template_name,
            {'form': self.form_class}
        )

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            mail_sent = bound_form.send_email()
            if mail_sent:
                success(
                    request,
                    'Email successfully sent.'
                )
                return redirect('home')
        return render(
            request,
            self.template_name,
            {'form': bound_form}
        )