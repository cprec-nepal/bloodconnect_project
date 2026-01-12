from django.urls import path
from . import views

app_name = 'bloodconnect_project'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.blood_bank_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('donor/', views.donor_register, name='donor_register'),
    path('sos/', views.sos_request_create, name='sos_request'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('map/', views.map_view, name='map'),
    path('bank/<int:bank_id>/', views.bank_detail, name='bank_detail'),
    path('api/blood-banks/', views.api_blood_banks, name='api_blood_banks'),
]
