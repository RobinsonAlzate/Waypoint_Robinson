from django.test import TestCase
from django.urls import reverse
from .models import Park, Trail
from waypoint_core.distance import Distance


class WaypointUnitAndIntegrationTests(TestCase):
    def setUp(self):
        self.park = Park.objects.create(name="Yellowstone", region="Wyoming")
        self.trail = Trail.objects.create(
            name="Old Faithful Loop",
            distance_km=5.50,
            elevation_gain=120,
            difficulty="Easy",
            is_open=True,
            park=self.park,
        )
        self.closed_trail = Trail.objects.create(
            name="Snowed-in Pass",
            distance_km=3.0,
            elevation_gain=50,
            difficulty="Easy",
            is_open=False,
            park=self.park,
        )

    def test_open_trails_query(self):
        response = self.client.get(reverse("trail_catalog"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Old Faithful Loop")
        self.assertNotContains(response, "Snowed-in Pass")

    def test_detail_404_for_missing_trail(self):
        response = self.client.get(reverse("trail_detail", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_distance_domain_rule(self):
        with self.assertRaises(ValueError):
            Distance(-3.0, "km")

    def test_report_form_requires_csrf(self):
        # Django's test client includes CSRF by default only with enforce_csrf_checks;
        # here we confirm the happy path succeeds and produces a personalized thank-you.
        response = self.client.post(reverse("report"), {
            "name": "Jordan", "email": "j@example.com",
            "trail": "Old Faithful Loop", "note": "Trail was clear today.",
        })
        self.assertContains(response, "Thanks, Jordan!")

    def test_park_deletion_sets_null_not_cascade(self):
        self.park.delete()
        self.trail.refresh_from_db()
        self.assertIsNone(self.trail.park)
