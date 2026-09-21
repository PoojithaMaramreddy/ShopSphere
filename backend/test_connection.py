from db_connection import get_connection


connection = get_connection()

if connection:
    cursor = connection.cursor()

    try:
        category_name = input("Enter category name: ")
        description = input("Enter category description: ")

        query = """
            INSERT INTO categories (category_name, description)
            VALUES (%s, %s);
        """

        values = (category_name, description)

        cursor.execute(query, values)

        connection.commit()

        print("Category inserted successfully!")
        print("New category ID:", cursor.lastrowid)

    except Exception as e:
        connection.rollback()
        print("Error inserting category:", e)

    finally:
        cursor.close()
        connection.close()
        print("Database connection closed!")