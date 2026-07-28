"""waypoint_core/itinerary.py — WP-105"""

from .distance import Distance


class Itinerary:
    def __init__(self):
        self._trails = []

    def add_trail(self, trail):
        self._trails.append(trail)

    @property
    def trails(self):
        return list(self._trails)  # defensive copy

    def total_distance(self, unit: str = "km") -> Distance:
        total = 0.0
        for t in self._trails:
            converted = t.distance.convert(unit)
            total += converted.magnitude
        return Distance(round(total, 2), unit)
