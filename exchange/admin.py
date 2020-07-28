from django.contrib import admin
from .models import Exchange

# This is for changing view of exchange gridview app in admin


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'api_key', 'secret_key', 'date']
    list_display_links = ['title', 'url']
    list_filter = ['title', 'date']
    search_fields = ['title']
    ordering = ['date', 'title']

    class Meta:
        model: Exchange


# Register your models here.
admin.site.register(Exchange, ExchangeAdmin)
