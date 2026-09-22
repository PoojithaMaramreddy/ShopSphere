import re
from datetime import date


def validate_name(name):
    if not name or not name.strip():
        return False

    if len(name.strip()) > 20:
        return False

    return bool(re.fullmatch(r"[A-Za-z]+(?: [A-Za-z]+)*", name.strip()))


def validate_email(email):
    if not email or not email.strip():
        return False

    if len(email) > 50:
        return False

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return bool(re.fullmatch(pattern, email))


def validate_phone(phone):
    if not phone:
        return False

    if len(phone) > 20:
        return False

    return phone.isdigit()


def validate_password(password):
    if not password or len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False

    if not re.search(r"[^A-Za-z0-9]", password):
        return False

    return True


def validate_dob(dob):
    if not isinstance(dob, date):
        return False

    if dob >= date.today():
        return False

    return True


def validate_price(price):
    try:
        return price >= 0
    except (TypeError, ValueError):
        return False


def validate_stock(stock_quantity):
    try:
        return stock_quantity >= 0
    except (TypeError, ValueError):
        return False


def validate_quantity(quantity):
    try:
        return quantity > 0
    except (TypeError, ValueError):
        return False


def validate_shipping_address(address):
    if not address or not address.strip():
        return False

    return True


def validate_payment_method(payment_method):
    allowed_methods = {
        "COD",
        "UPI",
        "CARD"
    }

    return payment_method in allowed_methods


def validate_order_status(status):
    allowed_statuses = {
        "pending",
        "confirmed",
        "shipped",
        "delivered",
        "cancelled"
    }

    return status in allowed_statuses


def validate_payment_status(payment_status):
    allowed_statuses = {
        "pending",
        "paid",
        "failed"
    }

    return payment_status in allowed_statuses
