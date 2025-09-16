import pytest
from fastapi.testclient import TestClient

from Backend.app.main import app
from Backend.app.models import User, Employee
from Backend.app.core.enums import RoleType
from Backend.app.core.db_setup import get_db
from Backend.app.routers import user as user_router
from Backend.app.core.security import get_password_hash


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
    app.dependency_overrides[user_router.require_admin] = override_require_admin
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    user = User(
        email="changepw@example.com",
        username="changepwuser",
        hashed_password=get_password_hash("oldpassword"),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.delete(user)
    db.commit()


def test_change_password_success(test_user: User, client):
    response = client.put(
        f"/users/{test_user.id}/change-password",
        json={"old_password": "oldpassword", "new_password": "newsecurepw"},
    )

    assert response.status_code == 200
    assert response.json() == {"detail": "Password updated successfully"}


def test_change_password_wrong_old_password(test_user: User, client):
    response = client.put(
        f"/users/{test_user.id}/change-password",
        json={"old_password": "wrongpassword", "new_password": "newsecurepw"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid old password or user not found"
