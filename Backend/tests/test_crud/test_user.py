from Backend.app.crud.user import authenticate_user
from Backend.app.models import User, Employee
from Backend.app.schemas.user import UserLoginSchema
from Backend.app.core.security import get_password_hash


def test_authenticate_user(db):
    test_employee = Employee()
    test_user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass123"),
        is_active=True,
        registration_completed=True,
        employee=test_employee,
    )
    db.add(test_user)
    db.commit()

    login_data = UserLoginSchema(username="testuser", password="testpass123")

    result = authenticate_user(db, login_data)

    assert result is not None
    assert result.username == "testuser"
    assert result.email == "test@example.com"
