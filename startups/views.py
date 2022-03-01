from django.shortcuts import render
from django.views.generic import (
    ListView
)

from .models import Startup

from config.utils import PageLinksMixin

class StartupListView(PageLinksMixin, ListView):
    model = Startup
    paginate_by = 3
