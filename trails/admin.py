from django.contrib import admin
from .models import Trail, Park


@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    list_display = ("name", "distance_km", "difficulty", "is_open", "park", "added")
    search_fields = ("name", "difficulty")
    list_filter = ("difficulty", "is_open", "park")


@admin.register(Park)
class ParkAdmin(admin.ModelAdmin):
    list_display = ("name", "region")
    search_fields = ("name", "region")
