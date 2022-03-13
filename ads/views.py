from decimal import Decimal as D

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import (
    ListView, View, DetailView, DeleteView, UpdateView, CreateView
)
from django.shortcuts import redirect
from django.urls import reverse_lazy

from config.utils import PageLinksMixin
from responses.models import Response

from .models import Ad
from .forms import AdForm

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
        if self.request.user.is_authenticated:
            context['ads_user_responded'] = self.request.user.responses.values_list('ad_id', flat=True)
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
        elif self.request_sort_by == 'small':
            self.ordering = 'share'
        elif self.request_sort_by == 'big':
            self.ordering = '-share'
        return self.ordering

class AdDetailView(DetailView):
    model = Ad
    queryset = (
        model.objects.select_related('user').select_related('startup'))

class UserAdsListView(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/user_ads.html'
    
    def get_queryset(self):
        self.queryset = (self.model.objects
            .select_related('user')
            .select_related('startup')
            .filter(user=self.request.user).order_by('-created'))
        return self.queryset

class AdCreateView(LoginRequiredMixin, View):
    model = Ad
    form = AdForm
    template_name = 'ads/ad_form.html'

    def get(self, request, **kwargs):
        user = request.user
        self.form = self.form(user)
        return render(request, self.template_name,
            {'form': self.form})

    def post(self, request, **kwargs):
        user = request.user
        bound_form = self.form(user, request.POST or None)
        if bound_form.is_valid():
            bound_form = bound_form.save(commit=False)
            bound_form.user = user
            bound_form.save()
            return redirect(bound_form)
        else:
            return render(request, self.template_name,
                {'form': bound_form})

class AdUpdateView(LoginRequiredMixin, View):
    model = Ad
    form = AdForm
    template_name = 'ads/ad_form.html'

    def get(self, request, **kwargs):
        user = request.user
        ad_obj = (self.model.objects
            .filter(user=user).get(slug=self.kwargs['slug']))
        self.form = self.form(user, instance=ad_obj)
        return render(request, self.template_name,
            {'form': self.form})

    def post(self, request, **kwargs):
        user = request.user
        ad_obj = (self.model.objects
            .filter(user=user).get(slug=self.kwargs['slug']))
        bound_form = self.form(
                user, request.POST or None, instance = ad_obj)
        if bound_form.is_valid():
            bound_form = bound_form.save(commit=False)
            bound_form.user = user
            bound_form.save()
            return redirect(bound_form)
        else:
            return render(request, self.template_name,
                {'form': bound_form})

class AdDeleteView(LoginRequiredMixin, DeleteView):
    queryset = Ad.objects.all()
    success_url = reverse_lazy('ads:user_ads')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            user=self.request.user
        )


class AdsIRespondedListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'ads/ads_i_responded.html'
    ordering = '-id'

    def get_queryset(self):
        self.queryset = (
            self.model.objects
            .filter(user=self.request.user)
            .select_related('ad__user'))
        return super().get_queryset()