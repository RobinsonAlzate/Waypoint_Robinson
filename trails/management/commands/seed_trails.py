from django.core.management.base import BaseCommand
from trails.models import Park, Trail


class Command(BaseCommand):
    help = "Seed sample parks and trails for manual testing (WP-503: at least 6 trails)."

    def handle(self, *args, **options):
        yellowstone, _ = Park.objects.get_or_create(name="Yellowstone", region="Wyoming")
        banff, _ = Park.objects.get_or_create(name="Banff", region="Alberta")

        sample = [
            dict(name="Old Faithful Loop", distance_km=5.50, elevation_gain=120, difficulty="Easy", is_open=True, park=yellowstone),
            dict(name="Mount Washburn Trail", distance_km=9.70, elevation_gain=520, difficulty="Hard", is_open=True, park=yellowstone),
            dict(name="Fairy Falls", distance_km=8.20, elevation_gain=90, difficulty="Moderate", is_open=False, park=yellowstone),
            dict(name="Johnston Canyon", distance_km=6.40, elevation_gain=250, difficulty="Moderate", is_open=True, park=banff),
            dict(name="Plain of Six Glaciers", distance_km=13.80, elevation_gain=680, difficulty="Expert", is_open=True, park=banff),
            dict(name="Sulphur Mountain", distance_km=11.00, elevation_gain=655, difficulty="Hard", is_open=True, park=banff),
        ]
        for data in sample:
            Trail.objects.get_or_create(name=data["name"], defaults=data)

        self.stdout.write(self.style.SUCCESS(f"Seeded {Trail.objects.count()} trails across {Park.objects.count()} parks."))
