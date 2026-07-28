from django.shortcuts import render, get_object_or_404
from .models import Trail, Park
from waypoint_core.trail import DayHike
from waypoint_core.distance import Distance


def catalog_view(request):
    # WP-605: open trails ordered by distance, rendered through the
    # Week 11 template unchanged.
    open_trails = Trail.objects.filter(is_open=True).order_by("distance_km")
    return render(request, "trails/catalog.html", {"trails": open_trails})


def trail_detail_view(request, trail_id):
    # Stretch (WP-605 optional): reuse Week 8's estimated_time() by
    # importing waypoint_core and building a DayHike from the DB row.
    trail = get_object_or_404(Trail, pk=trail_id)
    domain_trail = DayHike(
        trail_id=str(trail.id),
        name=trail.name,
        distance=Distance(float(trail.distance_km), "km"),
        elevation_gain_m=trail.elevation_gain,
        difficulty=trail.difficulty,
    )
    return render(request, "trails/trail_detail.html", {
        "trail": trail,
        "estimated_time": domain_trail.estimated_time(),
    })


def park_detail_view(request, park_id):
    # WP-705: cross-relation query -- trails in a given park.
    park = get_object_or_404(Park, pk=park_id)
    trails = park.trails.filter(is_open=True)
    return render(request, "trails/park_detail.html", {"park": park, "trails": trails})
