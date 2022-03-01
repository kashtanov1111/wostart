from django.shortcuts import render, redirect
from django.views.generic import (
    ListView
)

from .models import Startup

from config.utils import PageLinksMixin

class StartupListView(PageLinksMixin, ListView):
    model = Startup
    paginate_by = 3
    context_object_name = 'startup_list'
    queryset = model.objects.all()
    ordering = '-founded'
    default_pagination = 3

    def get(self, request, *args, **kwargs):
        self.request_paginate_by = self.request.GET.get('paginate_by')
        self.request_only_startups = (
            self.request.GET.get('only_websites'))
        self.request_sort_by = self.request.GET.get('sort_by')
        self.request_q = self.request.GET.get('q')
        self.request_clear_all = self.request.GET.get('clear_all')
        if self.request_clear_all == 'yes':
            return redirect('startups:startup_list')
        if (self.request_paginate_by is not None and 
            int(self.request_paginate_by) < 50):
            self.paginate_by = self.request_paginate_by
        else:
            self.paginate_by = self.default_pagination
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pag_by'] = self.request_paginate_by
        context['only_websites'] = self.request_only_startups 
        context['sort_by'] = self.request_sort_by
        context['query'] = self.request_q
        if context['pag_by'] is None:
            context['pag_by'] = str(self.default_pagination)
        return context

    def get_queryset(self):
        query = self.request_q
        if query:
            self.queryset = self.queryset.search(query)
        if self.request_only_startups == 'on':
            self.queryset = (self.queryset
                            .filter(web_site__isnull=False))
        return super().get_queryset()
    
    def get_ordering(self):
        if self.request_sort_by == 'old':
            self.ordering = 'founded'
        return self.ordering