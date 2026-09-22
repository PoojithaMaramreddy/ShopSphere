import os

import pymysql
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306))
        )

        print("Database connection successful!")

        return connection

    except pymysql.MySQLError as e:
        print("Database connection failed:", e)

        return None


if __name__ == "__main__":
    connection = get_connection()

    if connection:
        connection.close()
        print("Database connection closed!")