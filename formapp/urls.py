from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/<int:reset_id>/', views.ResetPassword, name='reset-password'),
]
