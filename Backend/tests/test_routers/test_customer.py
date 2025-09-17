import pytest
from fastapi.testclient import TestClient

from Backend.app.crud.customer import create_customer
from Backend.app.main import app
from Backend.app.models import User, Employee
from Backend.app.core.enums import CareLevel, Gender, RoleType
from Backend.app.core.db_setup import get_db
from Backend.app.schemas.customer import CustomerBaseSchema
from Backend.app.routers.customer import require_admin


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


def test_update_customer_success(db, client):
    customer_data = CustomerBaseSchema(
        first_name="John",
        last_name="Doe",
        key_number=12345,
        address="Main St",
        care_level=CareLevel.MEDIUM,
        gender=Gender.MALE,
        approved_hours=20.0,
        is_active=True,
    )
    customer = create_customer(db, customer_data)

    payload = {"approved_hours": 35.0}
    response = client.patch(f"/customers/{customer.id}", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == customer.id
    assert data["approved_hours"] == 35.0


def test_update_customer_not_found(client):
    payload = {"approved_hours": 50.0}
    response = client.patch("/customers/99999", json=payload)

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Customer with ID 99999 not found"
