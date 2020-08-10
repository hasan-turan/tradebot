from django.contrib import admin
from django.urls import path, re_path
from . import views

# Bu birden fazla uygulama olduğu zaman uygulamalara ait urlpatern isimleri(name=) karışmaması için
# tanımlanan bir değişkendir. Bu değişkene models içindeki get_detail_url fonksiyonu içinde erişilir.

app_name = "ccxtx"
urlpatterns = [
    path('', views.ccxtx_index, name='index'),
]
