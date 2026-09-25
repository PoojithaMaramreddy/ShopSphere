from backend.categories import (
    create_category,
    get_category_by_id,
    get_all_categories,
    update_category,
    delete_category,
)


def test_create_category():
    category_name = "Pytest Category"
    description = "Category created for testing."

    category_id = create_category(
        category_name,
        description,
    )

    assert category_id is not None

    deleted = delete_category(category_id)

    assert deleted == 1


def test_get_category_by_id():
    category_name = "Pytest Get Category"
    description = "Testing category retrieval."

    category_id = create_category(
        category_name,
        description,
    )

    assert category_id is not None

    category = get_category_by_id(category_id)

    assert category is not None
    assert category[0] == category_id
    assert category[1] == category_name
    assert category[2] == description

    deleted = delete_category(category_id)

    assert deleted == 1


def test_get_all_categories():
    categories = get_all_categories()

    assert categories is not None
    assert isinstance(categories, tuple)


def test_update_category():
    category_id = create_category(
        "Pytest Before Update",
        "Before update",
    )

    assert category_id is not None

    result = update_category(
        category_id,
        "Pytest After Update",
        "After update",
    )

    assert result == 1

    category = get_category_by_id(category_id)

    assert category is not None
    assert category[1] == "Pytest After Update"
    assert category[2] == "After update"

    deleted = delete_category(category_id)

    assert deleted == 1


def test_delete_category():
    category_id = create_category(
        "Pytest Delete Category",
        "Category to delete",
    )

    assert category_id is not None

    result = delete_category(category_id)

    assert result == 1

    category = get_category_by_id(category_id)

    assert category is None

