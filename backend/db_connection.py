import pymysql
def get_connection():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="2421",
            database="shopsphere",
            port=3306
        )
        print("Database connection successful!")
        return conn

    except pymysql.MySQLError as e:
        print("Database connection failed:", e)
        return None


if __name__ == "__main__":
    connection = get_connection()

    if connection:
        connection.close()
        print("Database connection closed!")