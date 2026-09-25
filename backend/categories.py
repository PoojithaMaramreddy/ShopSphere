from backend.db_connection import get_connection


def get_all_categories():
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute("""
                SELECT category_id, category_name, description, created_at
                FROM categories
            """)

            categories = cur.fetchall()
            return categories

        except Exception as e:
            print("Error fetching categories:", e)
            return []

        finally:
            cur.close()
            connection.close()


def get_category_by_id(category_id):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute("""
                SELECT category_id, category_name, description, created_at
                FROM categories
                WHERE category_id = %s
            """, (category_id,))

            category = cur.fetchone()
            return category

        except Exception as e:
            print("Error fetching category:", e)
            return None

        finally:
            cur.close()
            connection.close()


def create_category(category_name, description):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            query = """
                INSERT INTO categories
                (category_name, description)
                VALUES (%s, %s)
            """

            values = (category_name, description)

            cur.execute(query, values)
            connection.commit()

            return cur.lastrowid

        except Exception as e:
            connection.rollback()
            print("Error creating category:", e)
            return None

        finally:
            cur.close()
            connection.close()


def update_category(category_id, category_name, description):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            query = """
                UPDATE categories
                SET category_name = %s,
                    description = %s
                WHERE category_id = %s
            """

            values = (
                category_name,
                description,
                category_id
            )

            cur.execute(query, values)
            connection.commit()

            return cur.rowcount

        except Exception as e:
            connection.rollback()
            print("Error updating category:", e)
            return 0

        finally:
            cur.close()
            connection.close()


def delete_category(category_id):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            query = """
                DELETE FROM categories
                WHERE category_id = %s
            """

            cur.execute(query, (category_id,))
            connection.commit()

            return cur.rowcount

        except Exception as e:
            connection.rollback()
            print("Error deleting category:", e)
            return 0

        finally:
            cur.close()
            connection.close()