from django.contrib import admin

from core.models import Country, Name


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "region")
    search_fields = ("id", "code", "name", "region")


@admin.register(Name)
class NameAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country__code")
    search_fields = ("id", "name")
