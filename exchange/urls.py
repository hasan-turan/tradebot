from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', exchange_home_view),
    path('create/', exchange_create_view),
    path('update/', exchange_update_view),
    path('delete/', exchange_delete_view),
    path('detail/', exchange_detail_view),
]
