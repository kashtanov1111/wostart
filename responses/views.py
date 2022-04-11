import json
from ssl import OP_NO_RENEGOTIATION

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from config.utils import PageLinksMixin

from .models import Response
from ads.models import Ad

def response_button_view(request):
    if request.method == 'POST':
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            ad_slug = request.POST.get('ad_slug', None)
            ad_obj = get_object_or_404(Ad, slug=ad_slug)
            try:
                Response.objects.get(ad=ad_obj, user=request.user).delete()
                created = False
            except Response.DoesNotExist:
                Response.objects.create(ad=ad_obj, user=request.user)
                created = True
            return JsonResponse({'created': created,
                                'ad_slug': ad_slug})
    return redirect('ads:ad_list')

class ResponseListView(LoginRequiredMixin, PageLinksMixin, ListView):
    model = Response
    template_name = 'responses/response_list.html'
    ordering = '-id'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.request_paginate_by = self.request.GET.get('paginate_by')
        self.request_sort_by = self.request.GET.get('sort_by')
        self.request_ads = self.request.GET.get('ads')
        self.request_clear_all = self.request.GET.get('clear_all')
        if self.request_clear_all == 'yes':
            return redirect('responses:response_list')
        if (self.request_paginate_by is not None and 
            int(self.request_paginate_by) < 50):
            self.paginate_by = self.request_paginate_by
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_ads'] = self.request.user.ads.all()
        context['pag_by'] = self.request_paginate_by
        context['sort_by'] = self.request_sort_by
        context['ads'] = self.request_ads
        if context['pag_by'] is None:
            context['pag_by'] = str(self.paginate_by)
        return context

    def get_queryset(self):
        user_ad_ids = self.request.user.ads.values_list('id', flat=True)
        self.queryset = (
            self.model.objects
            .filter(ad_id__in=user_ad_ids)
            .select_related('user__profile')
            .select_related('ad'))
        if self.request_ads is not None and self.request_ads != 'all':
            self.queryset = self.queryset.filter(ad__slug=self.request_ads)
        return super().get_queryset()
    
    def get_ordering(self):
        if self.request_sort_by == 'old':
            self.ordering = 'id'
        return self.ordering