from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalog_view, name="trail_catalog"),
    path("<int:trail_id>/", views.trail_detail_view, name="trail_detail"),
    path("parks/<int:park_id>/", views.park_detail_view, name="park_detail"),
]
