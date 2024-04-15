from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
from django.views.generic import FormView
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.views import View
from django import forms
# from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from .models import Campaign, CampaignLocationInfo
from django.db import connection
from dao import insert_campaign_data, update_campaign_with_location_id, update_campaign_with_ticket_id, update_campaign_with_website_id
# from dao import insert_campaign_data


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required, Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(forms.Form):
    user = forms.CharField(
        label=_("User"),
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': _('User')})
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': _('Password')}),
        required=True
    )


class RegisterView(FormView):
    template_name = "user_register.html"
    form_class = UserRegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse('campaign_list'))

    def form_invalid(self, form):
        # render the same form with errors
        return render(self.request, self.template_name, {'form': form})


class LogInView(FormView):
    template_name = "user_login.html"
    form_class = UserLoginForm

    def form_valid(self, form):
        user_name = form.cleaned_data['user']
        password = form.cleaned_data['password']

        user = authenticate(
            self.request, username=user_name, password=password)

        if user is not None:
            login(self.request, user)
            return redirect(reverse('campaign_list'))
            # TODO: login authentication
            redirect_to = self.request.POST.get(
                settings.REDIRECT_FIELD_NAME, '')
            url_is_safe = is_safe_url(
                redirect_to,
                allowed_hosts=self.request.get_host(),
                require_https=self.request.is_secure())
            if url_is_safe:
                return redirect(redirect_to)
            return redirect(reverse('campaign_list'))
        else:
            error_message = _("使用者名稱或密碼錯誤！")
            form.add_error(None, error_message)
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
        # file_path = "/Users/kemal-wu/Desktop/d_test/music_data.json"
        # insert_campaign_data(file_path)
        # update_campaign_with_location_id(file_path)
        # update_campaign_with_ticket_id(file_path)
        # update_campaign_with_website_id(file_path)
        print("Data inserted!")

        campaigns = Campaign.objects.all()

        return render(request, 'campaign_list.html', {'campaigns': campaigns})


class QueryCampaignDetailsView(View):
    def get(self, request, uid, *args, **kwargs):
        campaign = get_object_or_404(Campaign, uid=uid)

        context = {
            'campaign': campaign,
        }

        return render(request, 'campaign_details.html', context)


class ModifyCampaignView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You are not authorized to access this page.")

        campaign_uid = kwargs.get('uid')
        campaign = get_object_or_404(
            Campaign, uid=campaign_uid)
        return render(request, 'campaign_modify.html', {'campaign': campaign})

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You are not authorized to modify this campaign.")

        campaign_uid = kwargs.get('uid')
        campaign = get_object_or_404(Campaign, uid=campaign_uid)
        campaign.title = request.POST.get('title', campaign.title)
        campaign.description_html = request.POST.get(
            'description', campaign.description_html)
        campaign.start_date = request.POST.get(
            'start_date', campaign.start_date)
        campaign.end_date = request.POST.get('end_date', campaign.end_date)
        # campaign.location = request.POST.get('location', campaign.location)
        location_name = request.POST.get('location', None)
        if location_name:
            location, created = CampaignLocationInfo.objects.get_or_create(
                location_name=location_name)
            campaign.location = location
        else:
            campaign.location = None
        campaign.save()

        return redirect('campaign_details', uid=campaign_uid)
