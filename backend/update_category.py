from db_connection import get_connection


connection = get_connection()

if connection:
    cursor = connection.cursor()

    try:
        category_id = int(input("Enter category ID: "))
        category_name = input("Enter new category name: ")
        description = input("Enter new description: ")

        query = """
            UPDATE categories
            SET category_name = %s,
                description = %s
            WHERE category_id = %s;
        """

        values = (category_name, description, category_id)

        cursor.execute(query, values)

        if cursor.rowcount > 0:
            connection.commit()
            print("Category updated successfully!")
        else:
            connection.rollback()
            print("Category not found!")

    except Exception as e:
        connection.rollback()
        print("Error updating category:", e)

    finally:
        cursor.close()
        connection.close()
        print("Database connection closed!")