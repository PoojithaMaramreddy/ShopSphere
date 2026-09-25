from datetime import date
from uuid import uuid4

from backend.orders import (
    create_order,
    get_order_by_id,
    get_user_orders,
    get_order_items,
    update_order_status,
    update_payment_status,
)

from backend.cart import (
    add_to_cart,
    get_cart_items,
)

from backend.users import create_user

from backend.products import (
    create_product,
    get_product_by_id,
    deactivate_product,
)

from backend.categories import (
    create_category,
    delete_category,
)


from random import randint


def create_test_user():
    phone = f"900000{randint(1000, 9999)}"

    unique_id = uuid4().hex[:8]

    return create_user(
        "Order",
        "Tester",
        f"pytest_order_{unique_id}@example.com",
        "Password@123",
        phone,
        date(2000, 1, 1),
    )


def create_test_product():
    unique_id = uuid4().hex[:8]

    category_id = create_category(
        f"Pytest Order Category {unique_id}",
        "Category for order tests",
    )

    product_id = create_product(
        f"Pytest Order Product {unique_id}",
        "Product for order testing",
        f"PYTEST-ORDER-{unique_id}",
        599.00,
        20,
        category_id,
    )

    return category_id, product_id


def cleanup_user(user_id):
    from backend.db_connection import get_connection

    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute(
                """
                DELETE oi
                FROM order_items oi
                JOIN orders o
                    ON oi.order_id = o.order_id
                WHERE o.user_id = %s
                """,
                (user_id,),
            )

            cur.execute(
                "DELETE FROM orders WHERE user_id = %s",
                (user_id,),
            )

            cur.execute(
                """
                DELETE ci
                FROM cart_items ci
                JOIN cart c
                    ON ci.cart_id = c.cart_id
                WHERE c.user_id = %s
                """,
                (user_id,),
            )

            cur.execute(
                "DELETE FROM cart WHERE user_id = %s",
                (user_id,),
            )

            cur.execute(
                "DELETE FROM users WHERE user_id = %s",
                (user_id,),
            )

            connection.commit()

        finally:
            cur.close()
            connection.close()


def test_create_order():
    user_id = create_test_user()
    category_id, product_id = create_test_product()

    add_to_cart(
        user_id,
        product_id,
        2,
    )

    order_id = create_order(
        user_id,
        "Hyderabad, Telangana",
        "COD",
    )

    assert order_id is not None

    order = get_order_by_id(
        user_id,
        order_id,
    )

    assert order is not None
    assert order[0] == order_id
    assert order[1] == user_id
    assert order[2] == "pending"
    assert order[3] == 1198.00
    assert order[4] == "Hyderabad, Telangana"
    assert order[5] == "COD"
    assert order[6] == "pending"

    deactivate_product(product_id)
    delete_category(category_id)
    cleanup_user(user_id)


def test_order_items():
    user_id = create_test_user()
    category_id, product_id = create_test_product()

    add_to_cart(
        user_id,
        product_id,
        1,
    )

    order_id = create_order(
        user_id,
        "Hyderabad, Telangana",
        "UPI",
    )

    assert order_id is not None

    items = get_order_items(
        user_id,
        order_id,
    )

    assert len(items) == 1
    assert items[0][1] == order_id
    assert items[0][2] == product_id
    assert items[0][4] == 1
    assert items[0][5] == 599.00
    assert items[0][6] == 599.00

    deactivate_product(product_id)
    delete_category(category_id)
    cleanup_user(user_id)


def test_user_orders():
    user_id = create_test_user()
    category_id, product_id = create_test_product()

    add_to_cart(
        user_id,
        product_id,
        1,
    )

    order_id = create_order(
        user_id,
        "Hyderabad, Telangana",
        "COD",
    )

    assert order_id is not None

    orders = get_user_orders(user_id)

    assert len(orders) >= 1
    assert orders[0][0] == order_id

    deactivate_product(product_id)
    delete_category(category_id)
    cleanup_user(user_id)


def test_update_order_status():
    user_id = create_test_user()
    category_id, product_id = create_test_product()

    add_to_cart(
        user_id,
        product_id,
        1,
    )

    order_id = create_order(
        user_id,
        "Hyderabad, Telangana",
        "COD",
    )

    result = update_order_status(
        order_id,
        "confirmed",
    )

    assert result == 1

    order = get_order_by_id(
        user_id,
        order_id,
    )

    assert order[2] == "confirmed"

    deactivate_product(product_id)
    delete_category(category_id)
    cleanup_user(user_id)


def test_update_payment_status():
    user_id = create_test_user()
    category_id, product_id = create_test_product()

    add_to_cart(
        user_id,
        product_id,
        1,
    )

    order_id = create_order(
        user_id,
        "Hyderabad, Telangana",
        "UPI",
    )

    result = update_payment_status(
        order_id,
        "paid",
    )

    assert result == 1

    order = get_order_by_id(
        user_id,
        order_id,
    )

    assert order[6] == "paid"

    deactivate_product(product_id)
    delete_category(category_id)
    cleanup_user(user_id)


def test_order_reduces_stock():
    user_id = create_test_user()
    category_id, product_id = create_test_product()

    product_before = get_product_by_id(product_id)

    stock_before = product_before[3]

    add_to_cart(
        user_id,
        product_id,
        3,
    )

    order_id = create_order(
        user_id,
        "Hyderabad, Telangana",
        "COD",
    )

    assert order_id is not None

    product_after = get_product_by_id(product_id)

    assert product_after[3] == stock_before - 3

    deactivate_product(product_id)
    delete_category(category_id)
    cleanup_user(user_id)


def test_empty_cart_order_fails():
    user_id = create_test_user()

    order_id = create_order(
        user_id,
        "Hyderabad, Telangana",
        "COD",
    )

    assert order_id is None

    cleanup_user(user_id)

