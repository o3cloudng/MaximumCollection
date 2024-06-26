from django.urls import path
from django.contrib.auth import views

from account.views import userlogin, signup, dashboard, logout_user, setup_profile

urlpatterns = [
    path('', userlogin, name="login"),
    path('signup/', signup, name="signup"),
    path('logout/', logout_user, name="logout_user"),
    # path('dashboard/', dashboard, name="dashboard"),
    path('setup_profile/', setup_profile, name="setup_profile"),
    path('settings/', setup_profile, name="settings"),
]
