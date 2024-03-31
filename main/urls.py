from django.urls import path, include
from .views import LogInView, DeleteCampaignView, QueryCampaignView, ModifyCampaignView




urlpatterns = [
    
    path("operation/login",LogInView.as_view(),name="user_login"),
    path('campaign/delete/<int:id>/', DeleteCampaignView.as_view(), name='delete_campaign'),
    path('campaigns/', QueryCampaignView.as_view(), name='query_campaigns'),
    path('campaign/modify/<int:id>/', ModifyCampaignView.as_view(), name='modify_campaign'),

]