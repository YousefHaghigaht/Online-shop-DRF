from django.urls import path
from . import views
from rest_framework.authtoken import views as authviews

app_name = 'accounts'

urlpatterns = [
    path('register/',views.UserRegisterView.as_view()),
    path('verify/',views.VerifyRegisterView.as_view()),
    path('create_token/',authviews.obtain_auth_token),
]