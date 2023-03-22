from .views import *
from django.urls import path

urlpatterns = [
    path("create_new_token/",create_new_token,name="create_new_token"),
    path("signup/",signup,name="signup"),
    path("verify_account/",verify_account,name="verify_account"),
    path("resend_verifiction/",resend_verifiction,name="resend_verifiction"),
    path("logout/",logout,name="logout"),
    path("get_weather_data/",get_weather_data,name="get_weather_data")
]
