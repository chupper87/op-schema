import pytest
from datetime import date, timedelta, datetime, time
from fastapi.testclient import TestClient
from Backend.app.main import app
from Backend.app.core.db_setup import get_db
from Backend.app.models import User, Employee
from Backend.app.core.enums import RoleType, ShiftType
from Backend.app.crud.schedule import create_schedule
from Backend.app.schemas.schedule import ScheduleBaseSchema
from Backend.app.dependencies import require_admin


def override_get_db(db):
    def _get_db_override():
        yield db

    return _get_db_override


def override_require_admin():
    dummy_user = User(
        id=999,
        username="adminuser",
        email="admin@example.com",
        is_superuser=True,
        is_active=True,
    )
    dummy_user.employee = Employee(role=RoleType.ADMIN, is_active=True)
    return dummy_user


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = override_get_db(db)
    app.dependency_overrides[require_admin] = override_require_admin
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def setup_schedules(db):
    today = date.today()
    schedules = []
    for i, shift in enumerate([ShiftType.MORNING, ShiftType.DAY, ShiftType.NIGHT]):
        schedule_dt = datetime.combine(today + timedelta(days=i), time.min)
        schema = ScheduleBaseSchema(
            date=schedule_dt,
            shift_type=shift,
            custom_shift=None,
        )
        schedules.append(create_schedule(db, schema))
    return schedules


def test_list_all_schedules(client, setup_schedules):
    response = client.get("/schedules")
    assert response.status_code == 200
    assert len(response.json()) >= 3


def test_filter_by_shift_type(client, setup_schedules):
    response = client.get("/schedules", params={"shift_type": "NIGHT"})
    assert response.status_code == 200
    data = response.json()
    assert all(s["shift_type"] == "NIGHT" for s in data)


def test_filter_by_date(client, setup_schedules):
    target_date = setup_schedules[0].date.isoformat()
    response = client.get("/schedules", params={"date": target_date})
    assert response.status_code == 200
    data = response.json()
    assert all(s["date"].startswith(target_date.split("T")[0]) for s in data)
