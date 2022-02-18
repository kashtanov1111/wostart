from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import (
    View
)

from .forms import CustomUserChangeForm, UserProfileForm

class UpdateUserProfileView(View):
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
            return redirect('profile:update_profile')
        else:
            return render(
                request,
                self.template_name,
                {'1form': bound_form1,
                '2form': bound_form2,
                'avatar_url': request.user.profile.avatar.url}
            )