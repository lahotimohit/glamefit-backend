from . import views
from django.urls import path

urlpatterns = [
    path('register', views.UserRegistration.as_view()),
    path('verify-otp', views.VerifyOTP.as_view()),
    path('login', views.UserLogin.as_view(), name='success'),
    path('profile', views.UserProfile.as_view()),
    path('request-reset/', views.RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('reset-password/<uuid:user_id>/<str:token>/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('billing-profile', views.BillingDetailsAPIView.as_view()),
    path("google-login/", views.GoogleLoginView.as_view(), name="google-login")
]
