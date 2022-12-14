from django.urls import path

from .views1 import *

urlpatterns = [
    path('normal_search', normal_search, name='normal_search'),
    path('file_upload', file_upload, name='file_upload'),
    path('search_info', search_info, name='search_info'),
    path('authentication', authentication, name='authentication'),
]
