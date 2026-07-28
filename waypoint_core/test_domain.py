import unittest
from waypoint_core.distance import Distance
from waypoint_core.trail import (
    DayHike, BackpackingRoute, TrailRun, GuidedDayHike, FakeTrail, Trail
)
from waypoint_core.itinerary import Itinerary


class TestDistancePhase1(unittest.TestCase):
    def test_rejects_negative(self):
        with self.assertRaises(ValueError):
            Distance(-3.0, "km")

    def test_convert_round_trip(self):
        d = Distance(10, "km")
        back = d.convert("mi").convert("km")
        self.assertAlmostEqual(back.magnitude, 10, delta=0.01)


class TestTrailPhase1(unittest.TestCase):
    def test_from_dict(self):
        data = {
            "id": "t1", "name": "Ridge Trail",
            "distance_magnitude": 5.0, "distance_unit": "km",
            "elevation_gain_m": 200, "difficulty": "Moderate",
        }
        t = DayHike.from_dict(data)
        self.assertEqual(t.name, "Ridge Trail")
        self.assertEqual(t.difficulty, "Moderate")

    def test_invalid_difficulty_raises(self):
        with self.assertRaises(ValueError):
            DayHike("t2", "Bad Trail", Distance(1, "km"), 10, "Impossible")

    def test_eq_by_id(self):
        t1 = DayHike("same-id", "A", Distance(1, "km"), 10, "Easy")
        t2 = BackpackingRoute("same-id", "Different name", Distance(99, "mi"), 999, "Expert")
        self.assertEqual(t1, t2)

    def test_default_unit_classmethod_scope(self):
        original = Trail.DEFAULT_UNIT
        try:
            Trail.DEFAULT_UNIT = "mi"
            t = DayHike.from_dict({
                "id": "t3", "name": "N", "distance_magnitude": 2,
                "elevation_gain_m": 5, "difficulty": "Easy",
            })
            self.assertEqual(t.distance.unit, "mi")
        finally:
            Trail.DEFAULT_UNIT = original


class TestItineraryPhase1(unittest.TestCase):
    def test_total_distance_and_isolation(self):
        it1 = Itinerary()
        it2 = Itinerary()
        it1.add_trail(DayHike("a", "A", Distance(3, "km"), 10, "Easy"))
        it1.add_trail(DayHike("b", "B", Distance(2, "km"), 10, "Easy"))
        it1.add_trail(DayHike("c", "C", Distance(5, "km"), 10, "Easy"))
        self.assertAlmostEqual(it1.total_distance().magnitude, 10.0)
        self.assertEqual(len(it2.trails), 0)  # adding to it1 never touched it2


class TestPhase2Polymorphism(unittest.TestCase):
    def test_cannot_instantiate_abstract(self):
        with self.assertRaises(TypeError):
            Trail("x", "X", Distance(1, "km"), 10, "Easy")

    def test_mixed_loop_and_duck_typing(self):
        trails = [
            DayHike("1", "Day", Distance(4, "km"), 100, "Easy"),
            BackpackingRoute("2", "Pack", Distance(20, "km"), 800, "Hard"),
            TrailRun("3", "Run", Distance(10, "km"), 50, "Moderate"),
            FakeTrail("Phantom Path"),
        ]
        results = [t.estimated_time() for t in trails]
        self.assertEqual(len(results), 4)
        self.assertIn("Backpacking", results[1])
        self.assertIn("Trail Run", results[2])
        self.assertEqual(results[3], "unknown (fake trail)")

    def test_guided_day_hike_extends_super(self):
        g = GuidedDayHike("4", "Guided", Distance(5, "km"), 100, "Easy", "Sam")
        self.assertIn("Guided by Sam", g.summary())
        self.assertIn("Day Hike", g.summary())

    def test_mro_is_predictable(self):
        mro_names = [c.__name__ for c in DayHike.__mro__]
        self.assertEqual(
            mro_names,
            ["DayHike", "Trail", "ABC", "ElevationMixin", "RatingMixin", "object"],
        )


class TestDistancePhase2Operators(unittest.TestCase):
    def test_add(self):
        self.assertEqual(Distance(3, "km") + Distance(2, "km"), Distance(5, "km"))

    def test_sort_with_lt(self):
        distances = [Distance(5, "km"), Distance(1, "km"), Distance(3, "km")]
        ordered = sorted(distances)
        self.assertEqual([d.magnitude for d in ordered], [1, 3, 5])

    def test_mixed_units_auto_convert(self):
        # documented behavior: right operand auto-converts into left's unit
        one_mile_in_km = Distance(1, "mi").convert("km").magnitude
        result = Distance(5, "km") + Distance(1, "mi")
        self.assertAlmostEqual(result.magnitude, 5 + one_mile_in_km, places=3)
        self.assertEqual(result.unit, "km")


if __name__ == "__main__":
    unittest.main(verbosity=2)
