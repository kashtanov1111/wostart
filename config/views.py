from pipes import Template
from django.views.generic import (
    TemplateView
)

class HomePageView(TemplateView):
    template_name = 'home.html'
