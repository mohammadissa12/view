from django.urls import path
from . import views

urlpatterns = [
    path('privacy/', views.privacy_policy, name='privacy'),
    path('login/', views.login_view, name='login'),
    path('delete_account/', views.delete_account_view, name='account_delete'),
]
