from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm
from django.conf import settings
from django.core.mail import send_mail

send_mail(
    'Тема',
    'Тело письма',
    settings.EMAIL_HOST_USER,
    [settings.SERVER_EMAIL],
    fail_silently=False,)


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
