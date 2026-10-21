
# ShopSphere — E-Commerce Backend System

ShopSphere is a backend-focused e-commerce system developed using **Python and MySQL**. It implements essential shopping operations, including user management, product management, shopping carts, order processing, and inventory updates.

The project demonstrates practical backend development through Python business logic, relational database design, data validation, transaction handling, and automated testing.

## Tech Stack

- **Programming Language:** Python
- **Database:** MySQL
- **Database Connectivity:** PyMySQL
- **Testing Framework:** pytest
- **Version Control:** Git and GitHub

## Key Features

### 1. User Management
- User registration and profile management
- Password validation and hashing
- Role-based user records
- Account activation and deactivation

### 2. Category and Product Management
- Create, retrieve, update, and delete categories
- Add, retrieve, and update products
- Product deactivation
- Inventory and stock management

### 3. Shopping Cart
- Add products to the cart
- Update product quantities
- Remove items from the cart
- Retrieve cart details
- Calculate cart totals

### 4. Order Management
- Generate orders from shopping cart items
- Validate product availability and stock
- Create order and order-item records
- Reduce inventory after order creation
- Calculate order totals
- Clear the cart after successful order creation
- Retrieve customer orders and order details
- Update order and payment statuses

## System Architecture

ShopSphere follows a modular Python backend architecture connected directly to a MySQL database using PyMySQL.

```text
          Python Backend
                 |
      Business Logic & Validation
                 |
              PyMySQL
                 |
                 v
            MySQL Database
```

The Python modules handle application operations, while MySQL manages persistent data storage and relational integrity.

## Database Design

The relational database contains eight primary tables:

| Table | Purpose |
|-------|---------|
| roles | Stores user roles |
| users | Stores customer and user information |
| categories | Organizes product categories |
| products | Stores product details and inventory |
| cart | Maintains shopping carts |
| cart_items | Stores products added to carts |
| orders | Stores customer orders |
| order_items | Stores individual items within orders |

### Database Concepts Implemented

- Primary and foreign keys
- Unique and check constraints
- Default values
- Database transactions
- Triggers
- Views
- Relational data integrity

### Database Triggers

Triggers support automatic timestamp updates and order-item subtotal calculations.

Examples:
- `user_update`
- `products_update`
- `cart_update`
- `orders_update`
- `order_items_insert`
- `order_items_update`

### Database Views

- `active_products_view`
- `order_summary_view`

These views simplify access to commonly required product and order information.

## Order Processing Workflow

The order management module coordinates several backend operations:

1. Retrieve items from the customer's shopping cart.
2. Check product availability and stock quantities.
3. Create the order and corresponding order-item records.
4. Calculate the order total.
5. Update product inventory.
6. Clear the shopping cart after successful order creation.

This workflow demonstrates coordination between Python business logic and related MySQL tables.

## Automated Testing

ShopSphere uses **pytest** for automated testing.

The test suite covers six functional areas:

- User management
- Input validation
- Category operations
- Product operations
- Shopping cart functionality
- Order processing

### Test Results

**48 tests passed** in the documented final test run.

To execute the tests from the project root:

```bash
pytest
```

Test execution requires the appropriate Python dependencies and database configuration.

## Project Structure

```text
ShopSphere/
|
|-- backend/
|   |-- db_connection.py
|   |-- users.py
|   |-- categories.py
|   |-- products.py
|   |-- cart.py
|   |-- orders.py
|
|-- docs/
|
|-- tests/
|   |-- test_users.py
|   |-- test_validation.py
|   |-- test_categories.py
|   |-- test_products.py
|   |-- test_cart.py
|   |-- test_orders.py
|
|-- requirements.txt
|-- .gitignore
|-- README.md
```

## Project Scope

ShopSphere is a backend-only implementation focused on Python programming and relational database operations.

It does not include a frontend, REST API, or web framework.

The project is intended to demonstrate backend business logic, database connectivity, validation, and testing rather than a deployed e-commerce website.

## Project Status

**Completed — Core Backend Implementation**

The primary backend modules, database functionality, and automated tests have been implemented.

## Skills Demonstrated

- Python backend development
- SQL and relational database design
- MySQL database integration
- PyMySQL
- CRUD operations
- Input validation and error handling
- Inventory and order processing
- Database constraints, triggers, views, and transactions
- Automated testing with pytest
- Git and GitHub version control
