import hashlib
import secrets

from db_connection import get_connection
from validation import (
    validate_name,
    validate_email,
    validate_phone,
    validate_password,
    validate_dob
)


def hash_password(password):
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(password, stored_password):
    try:
        salt_hex, hash_hex = stored_password.split(":")

        salt = bytes.fromhex(salt_hex)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100000
        )

        return secrets.compare_digest(
            password_hash.hex(),
            hash_hex
        )

    except (ValueError, TypeError):
        return False


def create_user(
    first_name,
    last_name,
    email,
    password,
    phone,
    dob,
    role_id=1
):
    if not validate_name(first_name):
        print("Invalid first name.")
        return None

    if not validate_name(last_name):
        print("Invalid last name.")
        return None

    if not validate_email(email):
        print("Invalid email.")
        return None

    if not validate_password(password):
        print("Invalid password.")
        return None

    if not validate_phone(phone):
        print("Invalid phone number.")
        return None

    if not validate_dob(dob):
        print("Invalid date of birth.")
        return None

    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            password_hash = hash_password(password)

            query = """
                INSERT INTO users
                (
                    first_name,
                    last_name,
                    email,
                    password_hash,
                    phone,
                    dob,
                    role_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                first_name,
                last_name,
                email,
                password_hash,
                phone,
                dob,
                role_id
            )

            cur.execute(query, values)
            connection.commit()

            return cur.lastrowid

        except Exception as e:
            connection.rollback()
            print("Error creating user:", e)
            return None

        finally:
            cur.close()
            connection.close()

    return None


def get_user_by_id(user_id):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute("""
                SELECT
                    user_id,
                    first_name,
                    last_name,
                    email,
                    password_hash,
                    phone,
                    dob,
                    role_id,
                    created_at,
                    updated_at,
                    is_active
                FROM users
                WHERE user_id = %s
            """, (user_id,))

            return cur.fetchone()

        except Exception as e:
            print("Error fetching user:", e)
            return None

        finally:
            cur.close()
            connection.close()

    return None


def get_all_users():
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute("""
                SELECT
                    user_id,
                    first_name,
                    last_name,
                    email,
                    phone,
                    dob,
                    role_id,
                    created_at,
                    updated_at,
                    is_active
                FROM users
            """)

            return cur.fetchall()

        except Exception as e:
            print("Error fetching users:", e)
            return []

        finally:
            cur.close()
            connection.close()

    return []


def update_user(
    user_id,
    first_name,
    last_name,
    email,
    phone,
    dob
):
    if not validate_name(first_name):
        print("Invalid first name.")
        return 0

    if not validate_name(last_name):
        print("Invalid last name.")
        return 0

    if not validate_email(email):
        print("Invalid email.")
        return 0

    if not validate_phone(phone):
        print("Invalid phone number.")
        return 0

    if not validate_dob(dob):
        print("Invalid date of birth.")
        return 0

    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            query = """
                UPDATE users
                SET
                    first_name = %s,
                    last_name = %s,
                    email = %s,
                    phone = %s,
                    dob = %s
                WHERE user_id = %s
            """

            values = (
                first_name,
                last_name,
                email,
                phone,
                dob,
                user_id
            )

            cur.execute(query, values)
            connection.commit()

            return cur.rowcount

        except Exception as e:
            connection.rollback()
            print("Error updating user:", e)
            return 0

        finally:
            cur.close()
            connection.close()

    return 0


def update_password(user_id, password):
    if not validate_password(password):
        print("Invalid password.")
        return 0

    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            password_hash = hash_password(password)

            query = """
                UPDATE users
                SET password_hash = %s
                WHERE user_id = %s
            """

            cur.execute(
                query,
                (password_hash, user_id)
            )

            connection.commit()

            return cur.rowcount

        except Exception as e:
            connection.rollback()
            print("Error updating password:", e)
            return 0

        finally:
            cur.close()
            connection.close()

    return 0


def deactivate_user(user_id):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            query = """
                UPDATE users
                SET is_active = 0
                WHERE user_id = %s
            """

            cur.execute(query, (user_id,))
            connection.commit()

            return cur.rowcount

        except Exception as e:
            connection.rollback()
            print("Error deactivating user:", e)
            return 0

        finally:
            cur.close()
            connection.close()

    return 0


def login_user(email, password):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute("""
                SELECT
                    user_id,
                    first_name,
                    last_name,
                    email,
                    password_hash,
                    phone,
                    dob,
                    role_id,
                    is_active
                FROM users
                WHERE email = %s
            """, (email,))

            user = cur.fetchone()

            if not user:
                return None

            if user[8] != 1:
                return None

            if not verify_password(password, user[4]):
                return None

            return user

        except Exception as e:
            print("Error during login:", e)
            return None

        finally:
            cur.close()
            connection.close()

    return None
