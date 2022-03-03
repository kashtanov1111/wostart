from ast import Delete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, DetailView, DeleteView,
)
from django.urls import reverse_lazy

from .models import Startup

from config.utils import PageLinksMixin

class StartupListView(PageLinksMixin, ListView):
    paginate_by = 3
    context_object_name = 'startup_list'
    queryset = Startup.objects.all()
    ordering = '-founded'

    def get(self, request, *args, **kwargs):
        self.request_paginate_by = self.request.GET.get('paginate_by')
        self.request_only_websites = (
            self.request.GET.get('only_websites'))
        self.request_sort_by = self.request.GET.get('sort_by')
        self.request_q = self.request.GET.get('q')
        self.request_clear_all = self.request.GET.get('clear_all')
        if self.request_clear_all == 'yes':
            return redirect('startups:startup_list')
        if (self.request_paginate_by is not None and 
            int(self.request_paginate_by) < 50):
            self.paginate_by = self.request_paginate_by
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pag_by'] = self.request_paginate_by
        context['only_websites'] = self.request_only_websites 
        context['sort_by'] = self.request_sort_by
        context['query'] = self.request_q
        if context['pag_by'] is None:
            context['pag_by'] = str(self.paginate_by)
        return context

    def get_queryset(self):
        query = self.request_q
        if query:
            self.queryset = self.queryset.search(query)
        if self.request_only_websites == 'on':
            self.queryset = (self.queryset
                            .filter(web_site__isnull=False))
        return super().get_queryset()
    
    def get_ordering(self):
        if self.request_sort_by == 'old':
            self.ordering = 'founded'
        return self.ordering

class StartupDetailView(DetailView):
    model = Startup
    

class UserStartupsListView(LoginRequiredMixin, ListView):
    model = Startup
    template_name = 'startups/user_startups.html'

    def get_queryset(self):
        self.queryset = (self.model.objects
            .filter(founder=self.request.user))
        return self.queryset

class StartupDeleteView(DeleteView):
    model = Startup
    success_url = reverse_lazy('startups:user_startups')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back'] = self.request.GET.get('back')
        return context