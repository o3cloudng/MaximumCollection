from django.urls import path
from django.contrib.auth import views

from admin.views import *

urlpatterns = [
    path('', waver, name="waver"),
]
