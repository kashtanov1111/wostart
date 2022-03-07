from csv import excel_tab
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin)
from django.forms import modelformset_factory
from django.forms.widgets import ClearableFileInput
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View, ListView, DetailView, DeleteView, UpdateView
)
from django.urls import reverse_lazy

from .models import Startup, StartupImage
from .forms import StartupForm, StartupCreateForm

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

class StartupDetailView(View):
    template_name = 'startups/startup_detail.html'
    model = Startup
    def get(self, request, **kwargs):
        try:
            startup_obj = (self.model.objects
                            .select_related('founder')
                            .get(slug=self.kwargs['slug']))
        except startup_obj.DoesNotExist:
            raise Http404()
        startup_images = startup_obj.images.exclude(image='')
        return render(request, self.template_name,
            {'startup': startup_obj,
            'startup_images': startup_images})

class UserStartupsListView(LoginRequiredMixin, ListView):
    model = Startup
    template_name = 'startups/user_startups.html'

    def get_queryset(self):
        self.queryset = (self.model.objects
            .filter(founder=self.request.user))
        return self.queryset

class StartupDeleteView(
    LoginRequiredMixin, DeleteView):
    queryset = Startup.objects.select_related('founder')
    success_url = reverse_lazy('startups:user_startups')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            founder=self.request.user
        )

class StartupUpdateView(
    LoginRequiredMixin, View):
    model = Startup
    template_name = 'startups/startup_update.html'
    form_class = StartupForm
    StartupFormSet = modelformset_factory(
        StartupImage, fields=('image',), extra=5, max_num=5,
        widgets={'image': ClearableFileInput(attrs=
        {'class': 'my-form-control form-control'})})
    def get(self, request, **kwargs):
        startup = get_object_or_404(
            self.model, slug=self.kwargs['slug'],
            founder=request.user)
        startup_images = startup.images.order_by('id')
        startup_images_additional = (
            [i for i in range(5 - len(startup_images))])
        return render(request, self.template_name,
            {'form_class': self.form_class(instance=startup),
            'formset': self.StartupFormSet(queryset=startup_images),
            'startup_images': startup_images,
            'startup_images_additional': startup_images_additional,
            })

    def post(self, request, **kwargs):
        startup = get_object_or_404(
            self.model, slug=self.kwargs['slug'],
            founder=request.user)
        startup_images = startup.images.order_by('id')
        startup_images_additional = (
            [i for i in range(5 - len(startup_images))])
        bound_form = self.form_class(
            request.POST, instance=startup)
        bound_formset = self.StartupFormSet(
            request.POST, request.FILES, queryset=startup_images)
        if bound_formset.is_valid() and bound_form.is_valid():
            instances = bound_formset.save(commit=False)
            for instance in instances:
                instance.startup = startup
                instance.save()
                # StartupImage.objects.update_or_create(image=instance.image, startup=startup)
            bound_form.save()
            return redirect(startup)
        else:
            return render(request, self.template_name,
            {'form_class': bound_form,
            'formset': bound_formset,
            'startup_images': startup_images,
            'startup_images_additional': startup_images_additional })

class StartupCreateView(LoginRequiredMixin, View):
    template_name = 'startups/startup_create.html'
    model = Startup
    form_class = StartupCreateForm
    def get(self, request, **kwargs):
        return render(request, self.template_name,
            {'form_class': self.form_class(),
            'create': 'yes'})

    def post(self, request, **kwargs):
        bound_form = self.form_class(
            request.POST or None, request.FILES or None)
        files = request.FILES.getlist('images')
        if bound_form.is_valid():
            user = request.user
            title = bound_form.cleaned_data['title']
            description = bound_form.cleaned_data['description']
            web_site = bound_form.cleaned_data['web_site']
            founded = bound_form.cleaned_data['founded']
            startup_obj = self.model.objects.create(
                title=title, description=description, web_site=web_site,
                founded=founded, founder=user
            )
            for f in files[:5]:
                StartupImage.objects.create(
                    startup=startup_obj, image=f)
            return redirect(startup_obj)
        else:
            return render(request, self.template_name,
            {'form_class': bound_form, 'create': 'yes'})

