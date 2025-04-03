from . import views
from django.urls import path

urlpatterns = [
    path('register', views.UserRegistration.as_view()),
    path('verify-otp', views.VerifyOTP.as_view()),
    path('login', views.UserLogin.as_view(), name='success'),
    path('profile', views.UserProfile.as_view()),
    path('billing-profile', views.BillingDetailsAPIView.as_view()),
    path("google-login/", views.GoogleLoginView.as_view(), name="google-login")
]
