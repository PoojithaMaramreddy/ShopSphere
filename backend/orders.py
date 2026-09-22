from db_connection import get_connection


def create_order(
    user_id,
    shipping_address,
    payment_method
):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            connection.begin()

            # Get user's cart
            cur.execute("""
                SELECT cart_id
                FROM cart
                WHERE user_id = %s
            """, (user_id,))

            cart = cur.fetchone()

            if not cart:
                print("Cart not found.")
                connection.rollback()
                return None

            cart_id = cart[0]

            # Get cart items
            cur.execute("""
                SELECT
                    ci.product_id,
                    ci.quantity,
                    p.price,
                    p.stock_quantity
                FROM cart_items ci
                JOIN products p
                    ON ci.product_id = p.product_id
                WHERE ci.cart_id = %s
                  AND p.is_active = 1
            """, (cart_id,))

            cart_items = cur.fetchall()

            if not cart_items:
                print("Cart is empty.")
                connection.rollback()
                return None

            # Check stock and calculate total
            total_amount = 0

            for item in cart_items:
                product_id = item[0]
                quantity = item[1]
                price = item[2]
                stock_quantity = item[3]

                if quantity > stock_quantity:
                    print(
                        f"Not enough stock for product {product_id}."
                    )
                    connection.rollback()
                    return None

                total_amount += price * quantity

            # Create order
            cur.execute("""
                INSERT INTO orders
                (
                    user_id,
                    order_status,
                    total_amount,
                    shipping_address,
                    payment_method,
                    payment_status
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                user_id,
                "pending",
                total_amount,
                shipping_address,
                payment_method,
                "pending"
            ))

            order_id = cur.lastrowid

            # Create order items and reduce stock
            for item in cart_items:
                product_id = item[0]
                quantity = item[1]
                price = item[2]

                cur.execute("""
                    INSERT INTO order_items
                    (
                        order_id,
                        product_id,
                        quantity,
                        unit_price,
                        subtotal
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    order_id,
                    product_id,
                    quantity,
                    price,
                    price * quantity
                ))

                cur.execute("""
                    UPDATE products
                    SET stock_quantity = stock_quantity - %s
                    WHERE product_id = %s
                """, (
                    quantity,
                    product_id
                ))

            # Clear cart after successful order creation
            cur.execute("""
                DELETE FROM cart_items
                WHERE cart_id = %s
            """, (cart_id,))

            connection.commit()

            return order_id

        except Exception as e:
            connection.rollback()
            print("Error creating order:", e)
            return None

        finally:
            cur.close()
            connection.close()


def get_order_by_id(user_id, order_id):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute("""
                SELECT
                    order_id,
                    user_id,
                    order_status,
                    total_amount,
                    shipping_address,
                    payment_method,
                    payment_status,
                    created_at,
                    updated_at
                FROM orders
                WHERE order_id = %s
                  AND user_id = %s
            """, (order_id, user_id))

            return cur.fetchone()

        except Exception as e:
            print("Error fetching order:", e)
            return None

        finally:
            cur.close()
            connection.close()


def get_user_orders(user_id):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute("""
                SELECT
                    order_id,
                    order_status,
                    total_amount,
                    shipping_address,
                    payment_method,
                    payment_status,
                    created_at
                FROM orders
                WHERE user_id = %s
                ORDER BY created_at DESC
            """, (user_id,))

            return cur.fetchall()

        except Exception as e:
            print("Error fetching orders:", e)
            return []

        finally:
            cur.close()
            connection.close()


def get_order_items(user_id, order_id):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute("""
                SELECT
                    oi.order_item_id,
                    oi.order_id,
                    oi.product_id,
                    p.product_name,
                    oi.quantity,
                    oi.unit_price,
                    oi.subtotal
                FROM order_items oi
                JOIN products p
                    ON oi.product_id = p.product_id
                JOIN orders o
                    ON oi.order_id = o.order_id
                WHERE oi.order_id = %s
                  AND o.user_id = %s
                ORDER BY oi.order_item_id
            """, (order_id, user_id))

            return cur.fetchall()

        except Exception as e:
            print("Error fetching order items:", e)
            return []

        finally:
            cur.close()
            connection.close()


def update_order_status(order_id, status):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute("""
                UPDATE orders
                SET order_status = %s
                WHERE order_id = %s
            """, (status, order_id))

            connection.commit()

            return cur.rowcount

        except Exception as e:
            connection.rollback()
            print("Error updating order status:", e)
            return 0

        finally:
            cur.close()
            connection.close()


def update_payment_status(order_id, payment_status):
    connection = get_connection()

    if connection:
        cur = connection.cursor()

        try:
            cur.execute("""
                UPDATE orders
                SET payment_status = %s
                WHERE order_id = %s
            """, (payment_status, order_id))

            connection.commit()

            return cur.rowcount

        except Exception as e:
            connection.rollback()
            print("Error updating payment status:", e)
            return 0

        finally:
            cur.close()
            connection.close()