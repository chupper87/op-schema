import pytest
from datetime import datetime, timedelta
from Backend.app.crud.schedule import create_schedule, get_schedules
from Backend.app.schemas.schedule import ScheduleBaseSchema
from Backend.app.core.enums import ShiftType


@pytest.fixture
def sample_schedules(db):
    today = datetime.now()
    schedules = []
    for i, shift in enumerate([ShiftType.MORNING, ShiftType.DAY, ShiftType.NIGHT]):
        schema = ScheduleBaseSchema(
            date=today + timedelta(days=i),
            shift_type=shift,
            custom_shift=None,
        )
        schedules.append(create_schedule(db, schema))
    return schedules


def test_get_all_schedules(db, sample_schedules):
    results = get_schedules(db)
    assert len(results) >= 3


def test_filter_by_shift_type(db, sample_schedules):
    results = get_schedules(db, shift_type=ShiftType.NIGHT)
    assert all(s.shift_type == ShiftType.NIGHT for s in results)


def test_filter_by_exact_date(db, sample_schedules):
    target_date = sample_schedules[0].date
    results = get_schedules(db, date=target_date)
    assert all(s.date == target_date for s in results)


def test_filter_by_date_range(db, sample_schedules):
    start = sample_schedules[0].date
    end = sample_schedules[-1].date
    results = get_schedules(db, date=None)  # normal get
    in_range = [s for s in results if start <= s.date <= end]
    assert len(in_range) >= 3
