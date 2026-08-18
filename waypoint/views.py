from django.shortcuts import render


def home_view(request):
    return render(request, "home.html", {"site_title": "Waypoint Trail Finder"})


def report_view(request):
    if request.method == "POST":
        reporter_name = request.POST.get("name", "").strip()
        trail_name = request.POST.get("trail", "").strip()
        note = request.POST.get("note", "").strip()

        # Stretch (WP-405 optional): reject an empty note server-side.
        if not note:
            return render(request, "report_form.html", {
                "error": "Please add a short note describing what you saw.",
                "name": reporter_name,
                "trail": trail_name,
            })

        return render(request, "thank_you.html", {
            "name": reporter_name or "Anonymous",
            "trail": trail_name,
        })
    return render(request, "report_form.html")


def search_view(request):
    query = request.GET.get("q", "")
    return render(request, "search.html", {"query": query})
