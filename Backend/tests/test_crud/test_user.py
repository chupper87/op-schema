import pytest
import datetime
from Backend.app.crud.user import (
    authenticate_user,
    invite_user,
    complete_registration,
    logout_user,
    delete_user,
    deactivate_user,
    activate_user,
    get_users,
    get_user_by_id,
    login_user,
)
from Backend.app.models import User, Employee, Token
from Backend.app.schemas.user import (
    UserLoginSchema,
    UserInviteSchema,
    UserCompleteRegistrationSchema,
)
from Backend.app.core.security import get_password_hash
from Backend.app.core.enums import Gender, RoleType


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


def test_invite_user(db):
    invite = UserInviteSchema(email="test@example.com", is_superuser=False)

    result = invite_user(db, invite)

    assert result is not None
    assert result.email == "test@example.com"


def test_complete_registration_success(db):
    user = User(
        email="test@example.com",
        registration_token="abc123",
        registration_completed=False,
        is_active=False,
    )
    user.employee = Employee(first_name="", last_name="", phone="")
    db.add(user)
    db.commit()
    db.refresh(user)

    schema = UserCompleteRegistrationSchema(
        registration_token="abc123",
        username="newuser",
        password="supersecret",
        first_name="Anna",
        last_name="Andersson",
        phone="123456789",
        gender=Gender.FEMALE,
        role=RoleType.EMPLOYEE,
        birth_date=datetime.date(1990, 1, 1),
    )
    result = complete_registration(db, schema)

    assert result.username == "newuser"
    assert result.is_active is True
    assert result.registration_completed is True
    assert result.registration_token is None
    assert result.employee.first_name == "Anna"
    assert result.employee.last_name == "Andersson"
    assert result.employee.phone == "123456789"
    assert result.employee.gender == "female"
    assert result.employee.role == RoleType.EMPLOYEE
    assert str(result.employee.birth_date) == "1990-01-01"
    assert result.hashed_password != "secret"


def test_complete_registration_invalid_token(db):
    schema = UserCompleteRegistrationSchema(
        registration_token="doesnotexist",
        username="nouser",
        password="irrelevant",
        first_name="Test",
        last_name="User",
        phone="000000",
        gender=Gender.MALE,
        role=RoleType.EMPLOYEE,
        birth_date=datetime.date(2000, 1, 1),
    )

    with pytest.raises(ValueError, match="Invalid registration token"):
        complete_registration(db, schema)


def test_logout_user(db):
    user = User(
        email="test@example.com",
        hashed_password="hashedpw",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = Token(token="abc123", user_id=user.id)
    db.add(token)
    db.commit()
    db.refresh(token)

    token_id = token.id

    logout_user(db, token)

    deleted = db.get(Token, token_id)
    assert deleted is None


def test_login_user_success(db):
    raw_password = "supersecret"
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash(raw_password),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    login_data = UserLoginSchema(username="testuser", password=raw_password)

    token = login_user(db, login_data)

    assert token is not None
    assert isinstance(token, Token)
    assert token.user_id == user.id


def test_login_user_invalid_credentials(db):
    user = User(
        email="wrong@example.com",
        username="wronguser",
        hashed_password=get_password_hash("rightpassword"),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()

    login_data = UserLoginSchema(username="wronguser", password="wrongpassword")

    token = login_user(db, login_data)

    assert token is None


def test_delete_user_success(db):
    user = User(
        email="test@example.com",
        username="test@example.com",
        hashed_password="hashedpw",
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    result = delete_user(db, user.id)

    assert result is True
    assert db.get(User, user.id) is None


def test_delete_user_not_found(db):
    result = delete_user(db, user_id=999)

    assert result is False


def test_deactivate_user(db):
    user = User(
        email="test@example.com",
        username="test@example.com",
        hashed_password="hashedpw",
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    result = deactivate_user(db, user.id)

    assert result is True
    db.refresh(user)
    assert user.is_active is False


def test_activate_user(db):
    user = User(
        email="test@example.com",
        username="test@example.com",
        hashed_password="hashedpw",
        is_active=False,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    result = activate_user(db, user.id)

    assert result is True
    db.refresh(user)
    assert user.is_active is True


def test_get_users_include_inactive(db):
    active_user = User(
        email="active@example.com",
        username="active",
        hashed_password="hashedpw",
        is_active=True,
        is_superuser=False,
    )
    inactive_user = User(
        email="inactive@example.com",
        username="inactive",
        hashed_password="hashedpw",
        is_active=False,
        is_superuser=False,
    )
    db.add_all([active_user, inactive_user])
    db.commit()

    users = get_users(db, include_inactive=True)

    emails = [u.email for u in users]
    assert "active@example.com" in emails
    assert "inactive@example.com" in emails


def test_get_user_by_id_active(db):
    user = User(
        email="active@example.com",
        username="active",
        hashed_password="hashedpw",
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    result = get_user_by_id(db, user.id, include_inactive=False)

    assert result is not None
    assert result.email == "active@example.com"


def test_get_user_by_id_inactive_filtered_out(db):
    user = User(
        email="inactive@example.com",
        username="inactive",
        hashed_password="hashedpw",
        is_active=False,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    result = get_user_by_id(db, user.id, include_inactive=False)

    assert result is None


def test_get_user_by_id_inactive_included(db):
    user = User(
        email="inactive@example.com",
        username="inactive",
        hashed_password="hashedpw",
        is_active=False,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    result = get_user_by_id(db, user.id, include_inactive=True)

    assert result is not None
    assert result.email == "inactive@example.com"
