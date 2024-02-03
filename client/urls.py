
from django.urls import path
from . import views

urlpatterns = [
    path('client-dashboard', views.client_dashboard, name="client-dashboard"),
    path('browse-articles', views.browse_articles, name="browse-articles"),
    path('account-management-client', views.account_management_client, name="account-management-client"),
    
    # Subscriptions
    path('subscription-locked', views.subscription_locked, name="subscription-locked"),
    path('subscription-plans', views.subscription_plans, name="subscription-plans"),
    path('create-subscription/<subID>/<plan>', views.create_subscription, name="create-subscription"),
    path('delete-subscription/<subID>', views.delete_subscription, name="delete-subscription"),
]
