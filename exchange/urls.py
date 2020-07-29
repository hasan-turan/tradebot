from django.contrib import admin
from django.urls import path, re_path
from . import views

# Bu birden fazla uygulama olduğu zaman uygulamalara ait urlpatern isimleri(name=) karışmaması için
# tanımlanan bir değişkendir. Bu değişkene models içindeki get_detail_url fonksiyonu içinde erişilir.

app_name = "exchange"
urlpatterns = [
    path('', views.exchange_index, name='index'),
    re_path(r'^(?P<id>[0-9])/$', views.exchange_detail, name='detail'),
    path('create/', views.exchange_create, name='create'),
    re_path(r'^(?P<id>[0-9])/update/', views.exchange_update, name='update'),
    re_path(r'^(?P<id>[0-9])/delete/', views.exchange_delete, name='delete'),

]
