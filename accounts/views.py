from allauth.account.views import PasswordChangeView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import (
    View, ListView, DetailView,
)

from .forms import CustomUserChangeForm, UserProfileForm
from config.utils import PageLinksMixin

from startups.models import Startup

class UpdateUserProfileView(LoginRequiredMixin, View):
    template_name = 'account/update_profile.html'
    form_class1 = CustomUserChangeForm
    form_class2 = UserProfileForm

    def check_avatar(self, request):
        if request.user.profile.avatar:
            avatar_url = request.user.profile.avatar.url
        else:
            avatar_url = None
        return avatar_url

    def get(self, request):
        return render(
            request,
            self.template_name,
            {'1form': self.form_class1(instance=request.user),
            '2form': self.form_class2(instance=request.user.profile),
            'avatar_url': self.check_avatar(request)}
        )

    def post(self, request):
        bound_form1 = self.form_class1(
                request.POST, request.FILES, instance=request.user)
        bound_form2 = self.form_class2(
            request.POST, request.FILES, instance=request.user.profile)
        if bound_form1.is_valid() and bound_form2.is_valid():
            bound_form1.save()
            bound_form2.save()
            return redirect(request.user)
        else:
            return render(
                request,
                self.template_name,
                {'1form': bound_form1,
                '2form': bound_form2,
                'avatar_url': self.check_avatar(request)}
            )

class UserListView(PageLinksMixin, ListView):
    template_name = 'users/user_list.html'
    context_object_name = 'user_list'
    queryset = (
        get_user_model().objects
        .select_related('profile'))
    paginate_by = 10
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
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pag_by'] = self.request_paginate_by
        context['only_startups'] = self.request_only_startups 
        context['sort_by'] = self.request_sort_by
        context['query'] = self.request_q
        if context['pag_by'] is None:
            context['pag_by'] = str(self.paginate_by)
        return context

    def get_queryset(self):
        query = self.request_q
        if query:
            self.queryset = self.queryset.search(query)
        if self.request_only_startups == 'on':
            self.queryset = (self.queryset
                            .filter(startups__isnull=False)
                            .distinct())
        return super().get_queryset()
    
    def get_ordering(self):
        if self.request_sort_by == 'old':
            self.ordering = 'date_joined'
        return self.ordering

class UserDetailView(View):
    model = get_user_model()
    template_name = 'users/user_detail.html'
    
    def get(self, request, **kwargs):
        try:
            user_obj = (self.model.objects
                .select_related('profile')
                .get(username=self.kwargs['username']))
        except ObjectDoesNotExist:
            raise Http404()
        person_startups = user_obj.startups.all()
        has_avatar = user_obj.profile.avatar
        return render(request, self.template_name,
            {'person': user_obj,
            'person_startups': person_startups,
            'has_avatar': has_avatar})

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context