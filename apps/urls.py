from django.urls import path
from main.views import LogInView, DeleteCampaignView, QueryCampaignView, ModifyCampaignView, QueryCampaignDetailsView, RegisterView

urlpatterns = [
    path("operation/register", RegisterView.as_view(), name="user_register"),
    path("operation/login", LogInView.as_view(), name="user_login"),
    path('operation/campaign/delete/<int:id>/',
         DeleteCampaignView.as_view(), name='delete_campaign'),
    path('operation/campaigns/', QueryCampaignView.as_view(), name='campaign_list'),
    path('operation/campaign/details/<str:uid>/',
         QueryCampaignDetailsView.as_view(), name='campaign_details'),
    path('operation/campaign/modify/<int:id>/',
         ModifyCampaignView.as_view(), name='modify_campaign'),

]
