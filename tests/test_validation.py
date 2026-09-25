from datetime import date

from backend.validation import (
    validate_name,
    validate_email,
    validate_phone,
    validate_password,
    validate_dob,
    validate_price,
    validate_stock,
    validate_quantity,
    validate_shipping_address,
    validate_payment_method,
    validate_order_status,
    validate_payment_status
)


def test_validate_name():
    assert validate_name("John") is True
    assert validate_name("John Doe") is True

    assert validate_name("") is False
    assert validate_name("John123") is False
    assert validate_name("John@") is False
    assert validate_name("A" * 21) is False


def test_validate_email():
    assert validate_email("test@example.com") is True
    assert validate_email("user123@gmail.com") is True

    assert validate_email("") is False
    assert validate_email("invalid-email") is False
    assert validate_email("test@") is False
    assert validate_email("test.com") is False


def test_validate_phone():
    assert validate_phone("9876543210") is True

    assert validate_phone("") is False
    assert validate_phone("98765abc10") is False
    assert validate_phone("987-654-3210") is False


def test_validate_password():
    assert validate_password("Password@123") is True

    assert validate_password("password") is False
    assert validate_password("PASSWORD@123") is False
    assert validate_password("Password@") is False
    assert validate_password("Password123") is False
    assert validate_password("Pass@1") is False


def test_validate_dob():
    assert validate_dob(date(2000, 1, 1)) is True

    assert validate_dob(date.today()) is False
    assert validate_dob("2000-01-01") is False


def test_validate_price():
    assert validate_price(599) is True
    assert validate_price(599.50) is True
    assert validate_price(0) is True

    assert validate_price(-1) is False


def test_validate_stock():
    assert validate_stock(10) is True
    assert validate_stock(0) is True

    assert validate_stock(-1) is False


def test_validate_quantity():
    assert validate_quantity(1) is True
    assert validate_quantity(10) is True

    assert validate_quantity(0) is False
    assert validate_quantity(-1) is False


def test_validate_shipping_address():
    assert validate_shipping_address("Hyderabad, Telangana") is True

    assert validate_shipping_address("") is False
    assert validate_shipping_address("   ") is False


def test_validate_payment_method():
    assert validate_payment_method("COD") is True
    assert validate_payment_method("UPI") is True
    assert validate_payment_method("CARD") is True

    assert validate_payment_method("CASH") is False


def test_validate_order_status():
    assert validate_order_status("pending") is True
    assert validate_order_status("confirmed") is True
    assert validate_order_status("shipped") is True
    assert validate_order_status("delivered") is True
    assert validate_order_status("cancelled") is True

    assert validate_order_status("invalid") is False


def test_validate_payment_status():
    assert validate_payment_status("pending") is True
    assert validate_payment_status("paid") is True
    assert validate_payment_status("failed") is True

    assert validate_payment_status("cancelled") is False
