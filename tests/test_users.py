from datetime import date

from backend.db_connection import get_connection
from backend.users import (
    hash_password,
    verify_password,
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    update_password,
    deactivate_user,
    login_user,
)


def test_password_hashing():
    password = "Password@123"

    stored_password = hash_password(password)

    assert stored_password != password
    assert ":" in stored_password


def test_password_verification():
    password = "Password@123"

    stored_password = hash_password(password)

    assert verify_password(password, stored_password) is True
    assert verify_password("WrongPassword@123", stored_password) is False


def test_create_user():
    email = "pytest_user@example.com"
    phone = "9000000001"

    user_id = create_user(
        "Pytest",
        "User",
        email,
        "Password@123",
        phone,
        date(2000, 1, 1),
    )

    assert user_id is not None

    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute(
                "DELETE FROM users WHERE user_id = %s",
                (user_id,),
            )

            connection.commit()

        finally:
            cur.close()
            connection.close()


def test_create_user_invalid_name():
    result = create_user(
        "John123",
        "User",
        "invalid_name@example.com",
        "Password@123",
        "9000000002",
        date(2000, 1, 1),
    )

    assert result is None


def test_create_user_invalid_email():
    result = create_user(
        "John",
        "User",
        "invalid-email",
        "Password@123",
        "9000000003",
        date(2000, 1, 1),
    )

    assert result is None


def test_create_user_invalid_password():
    result = create_user(
        "John",
        "User",
        "invalid_password@example.com",
        "password",
        "9000000004",
        date(2000, 1, 1),
    )

    assert result is None


def test_create_user_invalid_phone():
    result = create_user(
        "John",
        "User",
        "invalid_phone@example.com",
        "Password@123",
        "abc123",
        date(2000, 1, 1),
    )

    assert result is None


def test_create_user_invalid_dob():
    result = create_user(
        "John",
        "User",
        "invalid_dob@example.com",
        "Password@123",
        "9000000005",
        date.today(),
    )

    assert result is None


def test_get_user_by_id():
    email = "pytest_get@example.com"
    phone = "9000000006"

    user_id = create_user(
        "Get",
        "Test",
        email,
        "Password@123",
        phone,
        date(2000, 1, 1),
    )

    assert user_id is not None

    user = get_user_by_id(user_id)

    assert user is not None
    assert user[0] == user_id
    assert user[1] == "Get"
    assert user[2] == "Test"
    assert user[3] == email

    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute(
                "DELETE FROM users WHERE user_id = %s",
                (user_id,),
            )

            connection.commit()

        finally:
            cur.close()
            connection.close()


def test_get_all_users():
    users = get_all_users()

    assert users is not None
    assert isinstance(users, tuple)


def test_update_user():
    email = "pytest_update@example.com"
    phone = "9000000007"

    user_id = create_user(
        "Before",
        "Update",
        email,
        "Password@123",
        phone,
        date(2000, 1, 1),
    )

    assert user_id is not None

    result = update_user(
        user_id,
        "After",
        "Updated",
        "pytest_updated@example.com",
        "9000000008",
        date(1999, 5, 10),
    )

    assert result == 1

    user = get_user_by_id(user_id)

    assert user is not None
    assert user[1] == "After"
    assert user[2] == "Updated"
    assert user[3] == "pytest_updated@example.com"
    assert user[5] == "9000000008"

    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute(
                "DELETE FROM users WHERE user_id = %s",
                (user_id,),
            )

            connection.commit()

        finally:
            cur.close()
            connection.close()


def test_update_password():
    email = "pytest_password@example.com"
    phone = "9000000009"

    user_id = create_user(
        "Password",
        "Test",
        email,
        "Password@123",
        phone,
        date(2000, 1, 1),
    )

    assert user_id is not None

    result = update_password(
        user_id,
        "NewPassword@123",
    )

    assert result == 1

    user = get_user_by_id(user_id)

    assert user is not None
    assert verify_password(
        "NewPassword@123",
        user[4],
    ) is True

    assert verify_password(
        "Password@123",
        user[4],
    ) is False

    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute(
                "DELETE FROM users WHERE user_id = %s",
                (user_id,),
            )

            connection.commit()

        finally:
            cur.close()
            connection.close()