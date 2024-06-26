from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render,get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
from django.views.generic import FormView
from django.http import HttpResponse

from django.views import View
from django import forms
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


from .models import Campaign

class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        validators=[EmailValidator()],
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': _('Email')})
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': _('Password')}),
        required=True
    )

class LogInView(FormView):
    template_name = "user_login.html"
    form_class = EmailLoginForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
            redirect_to = self.request.POST.get(settings.REDIRECT_FIELD_NAME, '')
            url_is_safe = is_safe_url(redirect_to, allowed_hosts=self.request.get_host(), require_https=self.request.is_secure())

            if url_is_safe:
                return redirect(redirect_to)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            form.add_error(None, _("Invalid email or password"))
            return self.form_invalid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

class DeleteCampaignView(View):
    def get(self, request, *args, **kwargs):
        campaign_id = kwargs.get('id')
        campaign = get_object_or_404(Campaign, uid=campaign_id)
        campaign.delete()
        return HttpResponse(f"活動 {campaign_id} 已被刪除")

class QueryCampaignView(View):
    def get(self, request, *args, **kwargs):
        campaigns = Campaign.objects.all()
        return render(request, 'campaigns_list.html', {'campaigns': campaigns})

class ModifyCampaignView(View):
    def post(self, request, *args, **kwargs):
        campaign_id = kwargs.get('id')
        campaign = get_object_or_404(Campaign, uid=campaign_id)
        new_title = request.POST.get('title', campaign.title活動名稱)
        campaign.title活動名稱 = new_title
        campaign.save()
        return HttpResponse(f"活動 {campaign_id} 的標題已更新為 {new_title}")
