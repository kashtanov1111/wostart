from decimal import Decimal as D

from django.shortcuts import render
from django.views.generic import (
    ListView, View, DetailView, DeleteView, UpdateView, CreateView
)
from django.shortcuts import redirect

from config.utils import PageLinksMixin

from .models import Ad

class AdListView(PageLinksMixin, ListView):
    paginate_by = 3
    context_object_name = 'ad_list'
    queryset = (
        Ad.objects.select_related('startup').select_related('user'))
    ordering = '-created'

    def get(self, request, *args, **kwargs):
        self.request_paginate_by = self.request.GET.get('paginate_by')
        self.request_only_startups = (
            self.request.GET.get('only_startups'))
        self.request_sort_by = self.request.GET.get('sort_by')
        self.request_q = self.request.GET.get('q')
        self.request_only_who = self.request.GET.get('only_who')
        self.request_clear_all = self.request.GET.get('clear_all')
        self.request_share_min = self.request.GET.get('min')
        self.request_share_max = self.request.GET.get('max')
        if self.request_clear_all == 'yes':
            return redirect('ads:ad_list')
        if (self.request_paginate_by is not None and 
            int(self.request_paginate_by) < 50):
            self.paginate_by = self.request_paginate_by
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pag_by'] = self.request_paginate_by
        context['only_startups'] = self.request_only_startups 
        context['sort_by'] = self.request_sort_by
        context['query'] = self.request_q
        context['only_who'] = self.request_only_who
        context['min'] = self.request_share_min
        context['max'] = self.request_share_max
        if context['pag_by'] is None:
            context['pag_by'] = str(self.paginate_by)
        return context

    def get_queryset(self):
        query = self.request_q
        if query:
            self.queryset = self.queryset.search(query)
        if self.request_only_startups == 'on':
            self.queryset = (self.queryset
                            .filter(startup__isnull=False)
                            .distinct())
        if self.request_only_who == 'co_founders':
            self.queryset = (self.queryset
                            .filter(position='F'))
        elif self.request_only_who == 'employees':
            self.queryset = (self.queryset
                            .filter(position='E'))
        if self.request_share_min:
            min = D(self.request_share_min)
            self.queryset = (self.queryset
                            .filter(share__gte=min))
        if self.request_share_max:
            max = D(self.request_share_max)
            self.queryset = (self.queryset
                            .filter(share__lte=max))
        return super().get_queryset()
    
    def get_ordering(self):
        if self.request_sort_by == 'old':
            self.ordering = 'created'
        return self.ordering

class AdDetailView(DetailView):
    model = Ad
    