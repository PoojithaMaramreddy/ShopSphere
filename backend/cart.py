from backend.db_connection import get_connection


def get_or_create_cart(user_id):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            # Check if the user already has a cart
            cur.execute("""
                SELECT cart_id
                FROM cart
                WHERE user_id = %s
            """, (user_id,))

            cart = cur.fetchone()

            if cart:
                return cart[0]

            # Create a cart if one doesn't exist
            cur.execute("""
                INSERT INTO cart (user_id)
                VALUES (%s)
            """, (user_id,))

            connection.commit()

            return cur.lastrowid

        except Exception as e:
            connection.rollback()
            print("Error getting/creating cart:", e)
            return None

        finally:
            cur.close()
            connection.close()


def get_cart_items(user_id):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute("""
                SELECT
                    ci.cart_item_id,
                    ci.cart_id,
                    ci.product_id,
                    p.product_name,
                    p.price,
                    ci.quantity,
                    (p.price * ci.quantity) AS subtotal
                FROM cart_items ci
                JOIN cart c
                    ON ci.cart_id = c.cart_id
                JOIN products p
                    ON ci.product_id = p.product_id
                WHERE c.user_id = %s
                ORDER BY ci.cart_item_id
            """, (user_id,))

            return cur.fetchall()

        except Exception as e:
            print("Error fetching cart:", e)
            return []

        finally:
            cur.close()
            connection.close()


def add_to_cart(user_id, product_id, quantity):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            # Make sure the product exists and is active
            cur.execute("""
                SELECT product_id, stock_quantity
                FROM products
                WHERE product_id = %s
                  AND is_active = 1
            """, (product_id,))

            product = cur.fetchone()

            if not product:
                print("Product not found or inactive.")
                return False

            stock_quantity = product[1]

            # Check requested quantity
            if quantity <= 0:
                print("Quantity must be greater than zero.")
                return False

            if quantity > stock_quantity:
                print("Not enough stock.")
                return False

            # Get or create cart
            cur.execute("""
                SELECT cart_id
                FROM cart
                WHERE user_id = %s
            """, (user_id,))

            cart = cur.fetchone()

            if cart:
                cart_id = cart[0]
            else:
                cur.execute("""
                    INSERT INTO cart (user_id)
                    VALUES (%s)
                """, (user_id,))

                cart_id = cur.lastrowid

            # Check if product is already in cart
            cur.execute("""
                SELECT cart_item_id, quantity
                FROM cart_items
                WHERE cart_id = %s
                  AND product_id = %s
            """, (cart_id, product_id))

            existing_item = cur.fetchone()

            if existing_item:
                new_quantity = existing_item[1] + quantity

                if new_quantity > stock_quantity:
                    print("Not enough stock for total cart quantity.")
                    return False

                cur.execute("""
                    UPDATE cart_items
                    SET quantity = %s
                    WHERE cart_item_id = %s
                """, (new_quantity, existing_item[0]))

            else:
                cur.execute("""
                    INSERT INTO cart_items
                    (cart_id, product_id, quantity)
                    VALUES (%s, %s, %s)
                """, (cart_id, product_id, quantity))

            connection.commit()

            return True

        except Exception as e:
            connection.rollback()
            print("Error adding product to cart:", e)
            return False

        finally:
            cur.close()
            connection.close()


def update_cart_item(user_id, cart_item_id, quantity):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            if quantity <= 0:
                print("Quantity must be greater than zero.")
                return False

            cur.execute("""
                SELECT
                    ci.product_id
                FROM cart_items ci
                JOIN cart c
                    ON ci.cart_id = c.cart_id
                WHERE ci.cart_item_id = %s
                  AND c.user_id = %s
            """, (cart_item_id, user_id))

            item = cur.fetchone()

            if not item:
                print("Cart item not found.")
                return False

            product_id = item[0]

            cur.execute("""
                SELECT stock_quantity
                FROM products
                WHERE product_id = %s
                  AND is_active = 1
            """, (product_id,))

            product = cur.fetchone()

            if not product:
                print("Product not found or inactive.")
                return False

            if quantity > product[0]:
                print("Not enough stock.")
                return False

            cur.execute("""
                UPDATE cart_items
                SET quantity = %s
                WHERE cart_item_id = %s
            """, (quantity, cart_item_id))

            connection.commit()

            return cur.rowcount

        except Exception as e:
            connection.rollback()
            print("Error updating cart item:", e)
            return 0

        finally:
            cur.close()
            connection.close()


def remove_from_cart(user_id, cart_item_id):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute("""
                DELETE ci
                FROM cart_items ci
                JOIN cart c
                    ON ci.cart_id = c.cart_id
                WHERE ci.cart_item_id = %s
                  AND c.user_id = %s
            """, (cart_item_id, user_id))

            connection.commit()

            return cur.rowcount

        except Exception as e:
            connection.rollback()
            print("Error removing cart item:", e)
            return 0

        finally:
            cur.close()
            connection.close()


def clear_cart(user_id):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute("""
                DELETE ci
                FROM cart_items ci
                JOIN cart c
                    ON ci.cart_id = c.cart_id
                WHERE c.user_id = %s
            """, (user_id,))

            connection.commit()

            return cur.rowcount

        except Exception as e:
            connection.rollback()
            print("Error clearing cart:", e)
            return 0

        finally:
            cur.close()
            connection.close()