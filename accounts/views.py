from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.views.generic import (
    View, ListView, DetailView,
)

from .forms import CustomUserChangeForm, UserProfileForm
from config.utils import PageLinksMixin

class UpdateUserProfileView(LoginRequiredMixin, View):
    template_name = 'account/update_profile.html'
    form_class1 = CustomUserChangeForm
    form_class2 = UserProfileForm

    def get(self, request):
        if request.user.profile.avatar:
            avatar_url = request.user.profile.avatar.url
        else:
            avatar_url = None
        return render(
            request,
            self.template_name,
            {'1form': self.form_class1(instance=request.user),
            '2form': self.form_class2(instance=request.user.profile),
            'avatar_url': avatar_url}
        )

    def post(self, request):
        bound_form1 = self.form_class1(
                request.POST, request.FILES, instance=request.user)
        bound_form2 = self.form_class2(
            request.POST, request.FILES, instance=request.user.profile)
        if bound_form1.is_valid() and bound_form2.is_valid():
            bound_form1.save()
            bound_form2.save()
            return redirect('update_profile')
        else:
            return render(
                request,
                self.template_name,
                {'1form': bound_form1,
                '2form': bound_form2,
                'avatar_url': request.user.profile.avatar.url}
            )

class UserListView(PageLinksMixin, ListView):
    model = get_user_model()
    template_name = 'users/user_list.html'
    context_object_name = 'user_list'
    queryset = (
        model.objects
        .select_related('profile'))
    default_pagination = 3
    ordering = '-date_joined'

    def get(self, request, *args, **kwargs):
        self.request_paginate_by = self.request.GET.get('paginate_by')
        self.request_only_startups = (
            self.request.GET.get('only_startups'))
        self.request_sort_by = self.request.GET.get('sort_by')
        self.request_q = self.request.GET.get('q')
        self.request_clear_all = self.request.GET.get('clear_all')
        if self.request_clear_all == 'yes':
            return redirect('users:user_list')
        if (self.request_paginate_by is not None and 
            int(self.request_paginate_by) < 50):
            self.paginate_by = self.request_paginate_by
        else:
            self.paginate_by = self.default_pagination
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pag_by'] = self.request_paginate_by
        context['only_startups'] = self.request_only_startups 
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
                            .filter(profile__startups__isnull=False))
        return super().get_queryset()
    
    def get_ordering(self):
        if self.request_sort_by == 'old':
            self.ordering = 'date_joined'
        return self.ordering

class UserDetailView(DetailView):
    model = get_user_model()
    context_object_name = 'person'
    template_name = 'users/user_detail.html'
    
    def get_object(self):
        return get_object_or_404(
            self.model, username=self.kwargs['username'])