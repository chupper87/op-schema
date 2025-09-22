import pytest
from Backend.app.schemas.customer import CustomerBaseSchema
from Backend.app.crud.customer import (
    create_customer,
    get_customers,
    get_customer_by_id,
    delete_customer,
    search_customers,
    customer_exists,
)
from Backend.app.core.enums import Gender, CareLevel


def test_create_customer(db):
    customer_data = CustomerBaseSchema(
        first_name="John",
        last_name="Doe",
        key_number=555,
        address="123 Main St",
        care_level=CareLevel.HIGH,
        gender=Gender.MALE,
        approved_hours=40.0,
        is_active=True,
    )

    customer = create_customer(db, customer_data)
    assert customer.id is not None
    assert customer.first_name == customer_data.first_name
    assert customer.last_name == customer_data.last_name
    assert customer.key_number == customer_data.key_number
    assert customer.address == customer_data.address
    assert customer.care_level == customer_data.care_level
    assert customer.is_active is True  # Default value


def test_create_customer_duplicate_key_number(db):
    data = CustomerBaseSchema(
        first_name="Alice",
        last_name="Smith",
        key_number=123,
        address="Street 1",
        care_level=CareLevel.HIGH,
        gender=Gender.FEMALE,
        approved_hours=30.0,
        is_active=True,
    )
    create_customer(db, data)

    with pytest.raises(ValueError, match="Key number already exists"):
        create_customer(db, data)


def test_get_customers_active_only(db):
    active = CustomerBaseSchema(
        first_name="Active",
        last_name="User",
        key_number=321,
        address="Active St",
        care_level=CareLevel.MEDIUM,
        gender=Gender.MALE,
        approved_hours=20.0,
        is_active=True,
    )
    inactive = CustomerBaseSchema(
        first_name="Inactive",
        last_name="User",
        key_number=654,
        address="Inactive St",
        care_level=CareLevel.LOW,
        gender=Gender.FEMALE,
        approved_hours=15.0,
        is_active=False,
    )

    create_customer(db, active)
    create_customer(db, inactive)

    customers = get_customers(db)

    assert all(c.is_active for c in customers)
    assert not any(not c.is_active for c in customers)


def test_get_customers_include_inactive(db):
    data = CustomerBaseSchema(
        first_name="Carol",
        last_name="Inactive",
        key_number=987,
        address="Inactive St",
        care_level=CareLevel.LOW,
        gender=Gender.FEMALE,
        approved_hours=10.0,
        is_active=False,
    )
    create_customer(db, data)

    customers = get_customers(db, include_inactive=True)

    assert any(not c.is_active for c in customers)


def test_get_customer_by_id(db):
    data = CustomerBaseSchema(
        first_name="Diana",
        last_name="Prince",
        key_number=222,
        address="Themyscira",
        care_level=CareLevel.HIGH,
        gender=Gender.FEMALE,
        approved_hours=50.0,
        is_active=True,
    )
    customer = create_customer(db, data)

    found = get_customer_by_id(db, customer.id, include_inactive=True)
    assert found is not None
    assert found.id == customer.id


def test_get_customer_by_id_inactive_filtered_out(db):
    data = CustomerBaseSchema(
        first_name="Ed",
        last_name="Inactive",
        key_number=111,
        address="Hidden St",
        care_level=CareLevel.LOW,
        gender=Gender.MALE,
        approved_hours=15.0,
        is_active=False,
    )
    customer = create_customer(db, data)

    found = get_customer_by_id(db, customer.id, include_inactive=False)
    assert found is None


def test_get_customer_by_id_not_found(db):
    found = get_customer_by_id(db, 9999, include_inactive=True)
    assert found is None


def test_delete_customer_success(db):
    customer_data = CustomerBaseSchema(
        first_name="Test",
        last_name="Customer",
        key_number=777,
        address="Somewhere",
        care_level=CareLevel.MEDIUM,
        gender=Gender.MALE,
        approved_hours=10.0,
        is_active=True,
    )
    customer = create_customer(db, customer_data)

    result = delete_customer(db, customer.id)

    # Assert
    assert result is True

    deleted = get_customer_by_id(db, customer.id, include_inactive=True)
    assert deleted is None


def test_delete_customer_not_found(db):
    non_existing_id = 99999

    # Act
    result = delete_customer(db, non_existing_id)

    # Assert
    assert result is False


def test_search_customers(db):
    cust1 = CustomerBaseSchema(
        first_name="Alice",
        last_name="Wonderland",
        key_number=321,
        address="Fantasy Rd",
        care_level=CareLevel.LOW,
        gender=Gender.FEMALE,
        approved_hours=25.0,
        is_active=True,
    )
    cust2 = CustomerBaseSchema(
        first_name="Bob",
        last_name="Builder",
        key_number=876,
        address="Construction Ave",
        care_level=CareLevel.MEDIUM,
        gender=Gender.MALE,
        approved_hours=30.0,
        is_active=True,
    )

    alice = create_customer(db, cust1)
    bob = create_customer(db, cust2)

    # Search by first name
    results = search_customers(db, query="Alice")
    assert any(c.id == alice.id for c in results)
    assert all("Alice" in c.first_name for c in results)

    # Search by last name
    results = search_customers(db, query="Builder")
    assert any(c.id == bob.id for c in results)

    # Search by key_number
    results = search_customers(db, query="321")
    assert len(results) == 1
    assert results[0].id == alice.id

    # Search with no match
    results = search_customers(db, query="Nonexistent")
    assert results == []


def test_customer_exists(db):
    # Create a customer with a specific key_number
    customer_data = CustomerBaseSchema(
        first_name="Test",
        last_name="Exists",
        key_number=566,
        address="Exist St",
        care_level=CareLevel.HIGH,
        gender=Gender.MALE,
        approved_hours=10.0,
        is_active=True,
    )
    create_customer(db, customer_data)

    # Positive case → should exist
    assert customer_exists(db, key_number=566) is True

    # Negative case → pick a different number
    assert customer_exists(db, key_number=999) is False
