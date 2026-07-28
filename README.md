# Waypoint

A trail-finder and trip-planner. Pure-Python domain engine (`waypoint_core/`) wrapped in a Django site (`waypoint/`, `trails/`).

## Setup
```
python -m venv env
source env/bin/activate   # Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Visit http://127.0.0.1:8000/

## Run domain-engine tests only (no Django needed)
```
python -m unittest waypoint_core.test_domain -v
```

## Run full Django test suite
```
python manage.py test
```
