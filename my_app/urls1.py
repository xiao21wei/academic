from django.urls import path

from .views1 import *

urlpatterns = [
    path('normal_search', normal_search, name='normal_search'),
]
