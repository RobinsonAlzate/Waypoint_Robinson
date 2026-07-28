"""
waypoint_core/distance.py

Phase 1 (WP-101): value type holding magnitude + unit, negative values rejection,
read-only accessors, convert().

Phase 2 (WP-202): operator overloading. Design decision (documented per
acceptance criteria): mixed-unit operations AUTO-CONVERT the right-hand
operand into the left-hand operand's unit before comparing/combining.
This was chosen (over rejecting mixed units) because trip-planning totals
naturally mix km/mi input sources (e.g. imported GPX in km, manual entry
in mi), and forcing the caller to pre-convert everywhere would be more
error-prone than doing it once here.
"""

MILES_PER_KM = 1 / 1.60934


class Distance:
    #this validates the magnitud is not negative, also units km or mi, stores as a protected atributes: magintud &unit
    def __init__(self, magnitude: float, unit: str = "km"):
        if magnitude < 0:
            raise ValueError("Distance magnitude cannot be negative.")
        if unit not in ("km", "mi"):
            raise ValueError("Unit must be 'km' or 'mi'.")
        self._magnitude = float(magnitude)
        self._unit = unit

    @property
    def magnitude(self) -> float:
        return self._magnitude

    @property
    def unit(self) -> str:
        return self._unit

    def convert(self, target_unit: str) -> "Distance":
        #just for convertion purposes, rounded results in 4 decimals
        if target_unit not in ("km", "mi"):
            raise ValueError("Target unit must be 'km' or 'mi'.")
        if self._unit == target_unit:
            return Distance(self._magnitude, self._unit)
        # 1 mi = 1.60934 km
        if self._unit == "km" and target_unit == "mi":
            return Distance(round(self._magnitude / 1.60934, 4), "mi")
        else:  # mi -> km
            return Distance(round(self._magnitude * 1.60934, 4), "km")

    # ---- operator overloading (WP-202) ----

    def _as_unit(self, other: "Distance", unit: str) -> float:
        return other.magnitude if other.unit == unit else other.convert(unit).magnitude

    def __add__(self, other: "Distance") -> "Distance":
        if not isinstance(other, Distance):
            return NotImplemented
        other_val = self._as_unit(other, self._unit)
        return Distance(round(self._magnitude + other_val, 4), self._unit)

    def __sub__(self, other: "Distance") -> "Distance":
        if not isinstance(other, Distance):
            return NotImplemented
        other_val = self._as_unit(other, self._unit)
        return Distance(round(self._magnitude - other_val, 4), self._unit)

    def __eq__(self, other):
        if not isinstance(other, Distance):
            return False
        return abs(self._magnitude - self._as_unit(other, self._unit)) < 1e-6

    def __lt__(self, other: "Distance") -> bool:
        if not isinstance(other, Distance):
            return NotImplemented
        return self._magnitude < self._as_unit(other, self._unit)

    def __gt__(self, other: "Distance") -> bool:
        if not isinstance(other, Distance):
            return NotImplemented
        return self._magnitude > self._as_unit(other, self._unit)

    def __repr__(self) -> str:
        return f"Distance({self._magnitude}, '{self._unit}')"

    def __str__(self) -> str:
        return f"{self._magnitude} {self._unit}"

    def __hash__(self):
        # keep hashable in km-normalized form since __eq__ compares by value
        return hash(round(self.convert("km").magnitude, 6))
