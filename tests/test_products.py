from datetime import date
from uuid import uuid4

from backend.products import (
    create_product,
    get_product_by_id,
    get_all_products,
    update_product,
    deactivate_product,
)

from backend.categories import (
    create_category,
    delete_category,
)


def test_create_product():
    unique_id = uuid4().hex[:8]

    category_id = create_category(
        f"Pytest Product Category {unique_id}",
        "Category for product testing",
    )

    assert category_id is not None

    product_id = create_product(
        "Pytest Product",
        "Product created for testing",
        f"PYTEST-{unique_id}",
        999.00,
        10,
        category_id,
    )

    assert product_id is not None

    deactivate_product(product_id)

    delete_category(category_id)


def test_get_product_by_id():
    unique_id = uuid4().hex[:8]

    category_id = create_category(
        f"Pytest Get Product Category {unique_id}",
        "Category for retrieval testing",
    )

    product_id = create_product(
        "Pytest Get Product",
        "Testing product retrieval",
        f"PYTEST-GET-{unique_id}",
        599.00,
        20,
        category_id,
    )

    assert product_id is not None

    product = get_product_by_id(product_id)

    assert product is not None
    assert product[0] == product_id
    assert product[1] == "Pytest Get Product"
    assert product[2] == 599.00
    assert product[3] == 20
    assert product[4] == category_id
    assert product[5] == 1

    deactivate_product(product_id)

    delete_category(category_id)


def test_get_all_products():
    products = get_all_products()

    assert products is not None
    assert isinstance(products, tuple)


def test_update_product():
    unique_id = uuid4().hex[:8]

    category_id = create_category(
        f"Pytest Update Category {unique_id}",
        "Category for update testing",
    )

    product_id = create_product(
        "Pytest Update Product",
        "Product for update testing",
        f"PYTEST-UPDATE-{unique_id}",
        799.00,
        15,
        category_id,
    )

    assert product_id is not None

    result = update_product(
        product_id,
        "Pytest After Update",
        "After update",
        750.00,
        25,
        category_id,
    )

    assert result == 1

    product = get_product_by_id(product_id)

    assert product is not None
    assert product[1] == "Pytest After Update"
    assert product[2] == 750.00
    assert product[3] == 25
    assert product[4] == category_id

    deactivate_product(product_id)

    delete_category(category_id)


def test_deactivate_product():
    unique_id = uuid4().hex[:8]

    category_id = create_category(
        f"Pytest Deactivate Category {unique_id}",
        "Category for deactivate testing",
    )

    assert category_id is not None

    product_id = create_product(
        "Pytest Deactivate Product",
        "Product for deactivate testing",
        f"PYTEST-DEACTIVATE-{unique_id}",
        499.00,
        10,
        category_id,
    )

    assert product_id is not None

    result = deactivate_product(product_id)

    assert result == 1

    product = get_product_by_id(product_id)

    assert product is not None
    assert product[5] == 0

    delete_category(category_id)

