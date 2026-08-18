"""
waypoint_core/trail.py

Phase 1 (WP-102/103/104): encapsulated fields, DEFAULT_UNIT class var,
from_dict() alternate constructor, static validators, id-based __eq__.

Phase 2 (WP-201/202/203/204/205/206): abstract base class with abstract
estimated_time()/summary(), concrete DayHike / BackpackingRoute / TrailRun,
one further inheritance level (GuidedDayHike), two mixins composed in,
MRO-explainable multiple inheritance.
"""

from abc import ABC, abstractmethod
from .distance import Distance


class ElevationMixin:
    """Adds grade% calculation. Depends on .distance and .elevation_gain_m
    existing on the instance (duck-typed cooperation with Trail)."""

    def calculate_grade(self) -> float:
        if hasattr(self, "distance") and self.distance.magnitude > 0:
            dist_m = self.distance.convert("km").magnitude * 1000
            return round((self.elevation_gain_m / dist_m) * 100, 2)
        return 0.0


class RatingMixin:
    """Adds a simple star-rating collection. Cooperative __init__ so it
    can sit anywhere in the MRO chain."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ratings = []

    def add_rating(self, stars: int):
        if 1 <= stars <= 5:
            self._ratings.append(stars)

    @property
    def average_rating(self) -> float:
        if not self._ratings:
            return 0.0
        return round(sum(self._ratings) / len(self._ratings), 1)


ALLOWED_DIFFICULTIES = {"Easy", "Moderate", "Hard", "Expert"}


class Trail(ABC, ElevationMixin, RatingMixin):
    """Abstract base for all trail types.

    MRO for a class like `class DayHike(Trail)`:
        DayHike -> Trail -> ABC -> ElevationMixin -> RatingMixin -> object
    RatingMixin sits last among the mixins so its cooperative __init__
    (which calls super().__init__()) safely terminates the chain at object.
    """

    DEFAULT_UNIT = "km"

    def __init__(self, trail_id: str, name: str, distance: Distance,
                 elevation_gain_m: int, difficulty: str):
        super().__init__()
        self.trail_id = trail_id
        self.name = name
        self.distance = distance
        self.elevation_gain_m = elevation_gain_m
        self._set_difficulty(difficulty)

    def _set_difficulty(self, difficulty: str):
        if difficulty not in ALLOWED_DIFFICULTIES:
            raise ValueError(f"Invalid difficulty. Must be one of {ALLOWED_DIFFICULTIES}")
        self._difficulty = difficulty

    @property
    def difficulty(self) -> str:
        return self._difficulty

    def set_difficulty(self, difficulty: str):
        self._set_difficulty(difficulty)

    @classmethod
    def from_dict(cls, data: dict) -> "Trail":
        dist_val = data.get("distance_magnitude", 0.0)
        dist_unit = data.get("distance_unit", cls.DEFAULT_UNIT)
        distance_obj = Distance(dist_val, dist_unit)
        return cls(
            trail_id=data["id"],
            name=data["name"],
            distance=distance_obj,
            elevation_gain_m=data["elevation_gain_m"],
            difficulty=data["difficulty"],
        )

    @staticmethod
    def validate_elevation(elevation: int) -> bool:
        if elevation < 0:
            raise ValueError("Elevation gain cannot be negative.")
        return True

    def __eq__(self, other):
        if isinstance(other, Trail):
            return self.trail_id == other.trail_id
        return False

    def __hash__(self):
        return hash(self.trail_id)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.trail_id!r}, {self.name!r})"

    @abstractmethod
    def estimated_time(self) -> str:
        ...

    @abstractmethod
    def summary(self) -> str:
        ...


class DayHike(Trail):
    def estimated_time(self) -> str:
        # 4 km/h base pace + 30 min per 300m elevation gain
        hours = self.distance.convert("km").magnitude / 4.0
        extra_hours = (self.elevation_gain_m / 300.0) * 0.5
        total = round(hours + extra_hours, 1)
        return f"{total} hours"

    def summary(self) -> str:
        return f"Day Hike: {self.name} ({self.distance.magnitude} {self.distance.unit})"


class BackpackingRoute(Trail):
    def estimated_time(self) -> str:
        # slower pace under a full pack: 3 km/h
        hours = self.distance.convert("km").magnitude / 3.0
        return f"{round(hours, 1)} hours (Backpacking)"

    def summary(self) -> str:
        return f"Backpacking Route: {self.name}, {self.elevation_gain_m}m gain"


class TrailRun(Trail):
    def estimated_time(self) -> str:
        # faster pace: 8 km/h
        hours = self.distance.convert("km").magnitude / 8.0
        return f"{round(hours, 1)} hours (Trail Run)"

    def summary(self) -> str:
        return f"Trail Run: {self.name}"


class GuidedDayHike(DayHike):
    """One further inheritance level (WP-203): adds a guide_name field,
    calls super().__init__ to reuse DayHike's construction, and extends
    (not replaces) summary() via super()."""

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty, guide_name):
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)
        self.guide_name = guide_name

    def summary(self) -> str:
        base = super().summary()
        return f"{base} [Guided by {self.guide_name}]"


class FakeTrail:
    """WP-206: a duck-typed stand-in that inherits nothing from Trail,
    used to prove the polymorphic loop only cares about the interface,
    not the base class."""

    def __init__(self, name):
        self.name = name

    def estimated_time(self) -> str:
        return "unknown (fake trail)"

    def summary(self) -> str:
        return f"Fake Trail: {self.name}"
