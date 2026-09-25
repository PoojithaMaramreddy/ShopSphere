# ShopSphere — E-Commerce Database & Python Backend

ShopSphere is a small e-commerce learning project built using **Python and MySQL**.

The project focuses on learning how to design a relational database, connect Python to MySQL, implement backend business logic, validate data, write tests, and manage the project with Git and GitHub.

## 🎯 Project Goals

* Design and implement a relational MySQL database
* Understand tables, relationships, primary keys, and foreign keys
* Use constraints, triggers, and views
* Connect Python with MySQL using PyMySQL
* Implement e-commerce business logic in Python
* Practice validation and error handling
* Write automated tests using pytest
* Practice Git and GitHub workflow

## 🛠️ Tech Stack

* **Python**
* **MySQL**
* **PyMySQL**
* **pytest**
* **Git**
* **GitHub**

## 🏗️ Project Architecture

```text
Python Backend
      │
      │ PyMySQL
      ▼
MySQL Database
```

Python contains the application/business logic and communicates with the MySQL database through PyMySQL.

## 🗄️ Database

The ShopSphere database contains the following main tables:

* `roles`
* `users`
* `categories`
* `products`
* `cart`
* `cart_items`
* `orders`
* `order_items`

The database uses:

* Primary keys
* Foreign keys
* Unique constraints
* Check constraints
* Default values
* Transactions
* Triggers
* Views

## ⚙️ Database Triggers

The project includes triggers for automatically handling values such as:

* `updated_at` timestamps
* Order-item `subtotal` calculation

Examples include:

```text
user_update
products_update
cart_update
orders_update
order_items_insert
order_items_update
```

## 👁️ Database Views

The project includes views for commonly needed information:

* `active_products_view`
* `order_summary_view`

## 🛒 Main Features

### Users

* User registration
* Password validation
* Password hashing
* Role-based user records
* User activation/deactivation
* User profile operations

### Categories

* Create categories
* Retrieve categories
* Update categories
* Delete categories

### Products

* Create products
* Retrieve products
* Retrieve all products
* Update products
* Deactivate products
* Stock management

### Cart

* Add products to cart
* Update cart quantities
* Remove cart items
* View cart contents
* Calculate cart totals

### Orders

* Create orders from cart items
* Check product stock
* Reduce stock after order creation
* Create order items
* Calculate order totals
* Clear the cart after successful order creation
* Retrieve individual orders
* Retrieve user orders
* Retrieve order items
* Update order status
* Update payment status

## 🧪 Testing

The project uses **pytest** for automated testing.

The test suite covers:

* Users
* Validation
* Categories
* Products
* Cart
* Orders

Final test result:

```text
48 passed
```

## 📁 Project Structure

```text
ShopSphere/
│
├── backend/
│   ├── db_connection.py
│   ├── users.py
│   ├── categories.py
│   ├── products.py
│   ├── cart.py
│   └── orders.py
│
├── tests/
│   ├── test_users.py
│   ├── test_validation.py
│   ├── test_categories.py
│   ├── test_products.py
│   ├── test_cart.py
│   └── test_orders.py
│
├── database/
│   └── ...
│
└── README.md
```

## ▶️ Running the Tests

From the project root:

```bash
pytest
```

Expected result:

```text
48 passed
```

## 📚 What I Learned

This project was created primarily as a learning exercise.

Through ShopSphere, I practiced:

* Relational database design
* SQL and MySQL
* Foreign-key relationships
* Database constraints
* Transactions
* Triggers and views
* Python database connectivity
* Backend business logic
* Input validation
* Automated testing with pytest
* Debugging database-related errors
* Git and GitHub

## 🚫 Project Scope

ShopSphere is intentionally kept as a **Python + MySQL learning project**.

It does not use FastAPI or a frontend. The focus is on understanding Python backend logic and relational database concepts rather than building a complete production web application.

## 👩‍💻 Project Status

**Completed — Learning Project**

The core database, Python functionality, testing, and Git/GitHub workflow have been implemented and tested successfully.
