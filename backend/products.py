from db_connection import get_connection

def get_all_products():
    connection = get_connection()
    if connection:
        cur = connection.cursor()
        try:
            cur.execute("""SELECT product_id, product_name, price, stock_quantity, category_id, is_active FROM products""")
            products = cur.fetchall()
            return products
        except Exception as e:
            print("Error fetching products:", e)
            return []
        finally:
            cur.close()
            connection.close()

def get_product_by_id(product_id):
    connection = get_connection()
    if connection:
        cur = connection.cursor()
        try:
            cur.execute("""SELECT product_id, product_name, price, stock_quantity, category_id, is_active FROM products WHERE product_id = %s""", (product_id,))
            product = cur.fetchone()
            return product
        except Exception as e:
            print("Error fetching product:", e)
            return None
        finally:
            cur.close()
            connection.close()

def create_product(product_name, description, sku, price, stock_quantity, category_id):
    connection = get_connection()
    if connection:
        cur = connection.cursor()
        try:
            query = """INSERT INTO products(product_name, description, sku, price, stock_quantity, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (product_name, description, sku, price, stock_quantity, category_id)
            cur.execute(query, values)
            connection.commit()
            return cur.lastrowid
        except Exception as e:
            connection.rollback()
            print("Error creating product:", e)
            return None
        finally:
            cur.close()
            connection.close()

def update_product(product_id, product_name, description, price, stock_quantity, category_id):
    connection = get_connection()
    if connection:
        cur = connection.cursor()
        try:
            query = """UPDATE products SET product_name = %s,description = %s,price = %s,stock_quantity = %s,category_id = %s
                WHERE product_id = %s"""
            values = (product_name,description,price,stock_quantity,category_id,product_id)
            cur.execute(query, values)
            connection.commit()
            return cur.rowcount
        except Exception as e:
            connection.rollback()
            print("Error updating product:", e)
            return 0
        finally:
            cur.close()
            connection.close()

def deactivate_product(product_id):
    connection = get_connection()
    if connection:
        cur = connection.cursor()
        try:
            query = """UPDATE products SET is_active = 0 WHERE product_id = %s"""
            cur.execute(query, (product_id,))
            connection.commit()
            return cur.rowcount
        except Exception as e:
            connection.rollback()
            print("Error deactivating product:", e)
            return 0
        finally:
            cur.close()
            connection.close()