import time
import pytest

from db import (
    create_customer,
    get_customer_by_id,
    update_customer,
    delete_customer,
)


def build_customer_data():
    uniq = str(int(time.time() * 1000))
    return {
        "customer_group_id": 1,
        "store_id": 0,
        "language_id": 1,
        "firstname": "Test",
        "lastname": "User",
        "email": f"test_{uniq}@example.com",
        "telephone": f"+100000{uniq[-6:]}",
        "password": "test_password",
        "custom_field": "",
        "newsletter": 0,
        "ip": "127.0.0.1",
        "status": 1,
        "safe": 0,
        "token": "",
        "code": "",
    }


@pytest.fixture
def created_customer(connection):
    customer_data = build_customer_data()
    customer_id = create_customer(connection, customer_data)
    yield customer_id, customer_data

    existing = get_customer_by_id(connection, customer_id)
    if existing:
        delete_customer(connection, customer_id)


def test_create_customer(connection):
    customer_data = build_customer_data()

    customer_id = create_customer(connection, customer_data)
    customer = get_customer_by_id(connection, customer_id)

    try:
        assert customer["customer_id"] == customer_id
        assert customer["firstname"] == customer_data["firstname"]
        assert customer["lastname"] == customer_data["lastname"]
        assert customer["email"] == customer_data["email"]
        assert customer["telephone"] == customer_data["telephone"]
    finally:
        delete_customer(connection, customer_id)


def test_update_existing_customer(connection, created_customer):
    customer_id, _ = created_customer

    updated_data = {
        "firstname": "UpdatedName",
        "lastname": "UpdatedLast",
        "email": "updated@example.com",
        "telephone": "+1234567890",
    }

    affected = update_customer(connection, customer_id, updated_data)
    customer = get_customer_by_id(connection, customer_id)

    assert affected == 1
    assert customer is not None
    assert customer["firstname"] == updated_data["firstname"]
    assert customer["lastname"] == updated_data["lastname"]
    assert customer["email"] == updated_data["email"]
    assert customer["telephone"] == updated_data["telephone"]


def test_update_non_existing_customer(connection):
    non_existing_id = 999999999

    updated_data = {
        "firstname": "NoName",
        "lastname": "NoLast",
        "email": "no@example.com",
        "telephone": "+0000000000",
    }

    affected = update_customer(connection, non_existing_id, updated_data)

    assert affected == 0


def test_delete_existing_customer(connection):
    customer_data = build_customer_data()
    customer_id = create_customer(connection, customer_data)

    affected = delete_customer(connection, customer_id)
    customer = get_customer_by_id(connection, customer_id)

    assert affected == 1
    assert customer is None


def test_delete_non_existing_customer(connection):
    non_existing_id = 999999999

    affected = delete_customer(connection, non_existing_id)

    assert affected == 0
