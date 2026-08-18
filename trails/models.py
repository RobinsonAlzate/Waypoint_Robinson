from django.db import models


class Park(models.Model):
    """WP-701: a trail belongs to a park."""
    name = models.CharField(max_length=150)
    region = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.region})"


class Trail(models.Model):
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Moderate", "Moderate"),
        ("Hard", "Hard"),
        ("Expert", "Expert"),
    ]

    name = models.CharField(max_length=150)
    distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    elevation_gain = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    is_open = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)
    # WP-702: on_delete=SET_NULL (not CASCADE) -- deleting a Park should not
    # wipe out the trails that belong to it; they become "unassigned"
    # instead of disappearing from the catalog. null/blank=True so existing
    # rows created before this field existed remain valid.
    park = models.ForeignKey(
        Park, on_delete=models.SET_NULL, related_name="trails",
        null=True, blank=True,
    )

    def __str__(self):
        park_name = self.park.name if self.park else "No Park"
        return f"{self.name} ({self.distance_km} km) - {park_name}"
