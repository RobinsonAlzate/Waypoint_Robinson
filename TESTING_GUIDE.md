# Waypoint — Phase-by-Phase Testing Guide

Every phase from the assignment is implemented and has already been verified
running (14 domain tests + 19 total Django tests + live page hits, all green).
This is the map of **which files satisfy which week**, and how to test
each phase 

---

## Phase 1 (Week 7) — Domain model: classes & objects
**Files:** `waypoint_core/distance.py`, `waypoint_core/trail.py` (base parts),
`waypoint_core/itinerary.py`

**Test (no Django, no venv needed):**
```
python -m unittest waypoint_core.test_domain -v
```
Look at the `TestDistancePhase1`, `TestTrailPhase1`, `TestItineraryPhase1`
classes specifically — those map 1:1 to WP-101..105.

**Try interactively:**
```python
from waypoint_core.distance import Distance
from waypoint_core.trail import DayHike
d = Distance(5, "km")
d.convert("mi")                     # round trip
DayHike.from_dict({"id": "t1", "name": "Ridge", "distance_magnitude": 5,
                    "elevation_gain_m": 200, "difficulty": "Moderate"})
```

---

## Phase 2 (Week 8) — Inheritance, polymorphism, operators
**Files:** same `waypoint_core/trail.py` (ABC + mixins + subclasses),
`waypoint_core/distance.py` (operator overloads)

**Test:**
```
python -m unittest waypoint_core.test_domain -v
```
See `TestPhase2Polymorphism` and `TestDistancePhase2Operators`.

**Try interactively:**
```python
from waypoint_core.trail import DayHike, BackpackingRoute, TrailRun, FakeTrail
print(DayHike.__mro__)              # show the MRO for  PR description
for t in [DayHike(...), FakeTrail("Phantom")]:
    print(t.estimated_time())       # polymorphic + duck-typed in one loop
```

---

## Phase 3 (Week 9) — Django setup
**Files:** `manage.py`, `waypoint/settings.py`, `.gitignore`, `requirements.txt`, `README.md`

**Test:**
```
python -m venv env && source env/bin/activate   # Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```
Visit http://127.0.0.1:8000/ — Django welcome page 
---

## Phase 4 (Week 10) — Views, URLs, report form
**Files:** `waypoint/views.py`, `waypoint/urls.py`, `templates/home.html`,
`templates/report_form.html`, `templates/thank_you.html`, `templates/search.html`

**Test :**
- Load `/` → home page.
- Load `/report/`, submit the form → thank-you page 


---

## Phase 5 (Week 11) — Catalog templates
**Files:** `templates/base.html`, `templates/partials/navbar.html`,
`templates/partials/footer.html`, `templates/trails/catalog.html`,
`static/css/style.css`

**Test :**
- Edit `templates/partials/navbar.html` — confirm every page changes.
- Load `/trails/` — table renders with `forloop.counter` row numbers and
  `floatformat:1` distances.



---

## Phase 6 (Week 12) — Database, models, admin
**Files:** `trails/models.py` (Trail), `trails/admin.py`, `trails/views.py`
(`catalog_view`), `trails/migrations/0001_initial.py`,
`trails/management/commands/seed_trails.py`

**Test:**
```
python manage.py makemigrations trails
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_trails      # adds 6 sample trails across 2 parks
python manage.py runserver
```
- Log into `/admin/`
- Uncheck "is open" on a trail in the admin → confirm it vanishes from the
  public catalog.

---

## Phase 7 (Week 13) — Relationships & ForeignKey
**Files:** `trails/models.py` (Park + FK), `trails/views.py`
(`park_detail_view`), `trails/urls.py`, `templates/trails/park_detail.html`,
catalog's park column

**Test it:**
- In `/admin/`, create a Park, assign it to a Trail.
- Load `/trails/` — the trail's park now links to `/trails/parks/<id>/`.
- Loaded that park page — lists only its open trails (`park.trails.filter(...)`).

---

## Phase 8 (Week 14) — Hardening & handoff
**Files:** `trails/tests.py`, this `TESTING_GUIDE.md`, `README.md`




---

