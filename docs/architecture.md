# ShopSphere — E-Commerce Backend

## 1. Project Overview

ShopSphere is a small e-commerce backend project built for learning backend development using Python and MySQL.

The project focuses on understanding:

* Relational database design
* SQL and MySQL
* Python database connectivity
* Backend business logic
* REST APIs
* Authentication
* Transactions
* Validation
* Testing
* Git and version control

The project will initially focus on the backend only. A frontend may be added later.

---

## 2. Project Goals

The main goals of ShopSphere are:

1. Design a proper relational database.
2. Implement the database using MySQL.
3. Connect Python with MySQL using PyMySQL.
4. Build backend functionality using Python.
5. Introduce FastAPI for REST API development.
6. Implement user authentication and authorization.
7. Implement products, categories, cart, and orders.
8. Practice database constraints, triggers, views, and transactions.
9. Test backend functionality.
10. Maintain the project using Git and GitHub.

The project should remain small enough to complete without becoming unnecessarily complex.

---

## 3. Technology Stack

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Backend programming       |
| MySQL      | Relational database       |
| PyMySQL    | Python-MySQL connectivity |
| FastAPI    | REST API framework        |
| Git        | Version control           |
| GitHub     | Remote repository         |

---

## 4. High-Level Architecture

```
Client
   │
   ▼
FastAPI / Python Backend
   │
   ▼
PyMySQL
   │
   ▼
MySQL Database
```

The backend will contain the business logic and communicate with MySQL through PyMySQL.

---

# 5. Database Architecture

## 5.1 Roles

The `roles` table defines the roles available in the application.

```text
roles
├── role_id
└── role_name
```

### Fields

| Field     | Type        | Constraints        |
| --------- | ----------- | ------------------ |
| role_id   | INT         | PK, AUTO_INCREMENT |
| role_name | VARCHAR(20) | NOT NULL, UNIQUE   |

### Initial Roles

* customer
* admin

### Relationship

```
roles 1 ───── N users
```

A role can belong to many users.

Normal user registration should assign the `customer` role.

Users must not be allowed to register themselves as administrators.

---

## 5.2 Users

The `users` table stores customer and administrator account information.

```
users
├── user_id
├── first_name
├── last_name
├── email
├── password_hash
├── phone
├── dob
├── role_id
├── created_at
└── updated_at
```

### Fields

| Field         | Type         | Constraints               |
| ------------- | ------------ | ------------------------- |
| user_id       | INT          | PK, AUTO_INCREMENT        |
| first_name    | VARCHAR(50)  | NOT NULL                  |
| last_name     | VARCHAR(50)  | NOT NULL                  |
| email         | VARCHAR(100) | NOT NULL, UNIQUE          |
| password_hash | VARCHAR(...) | NOT NULL                  |
| phone         | VARCHAR(20)  | NOT NULL, UNIQUE          |
| dob           | DATE         | NOT NULL                  |
| role_id       | INT          | NOT NULL, FK              |
| created_at    | DATETIME     | DEFAULT CURRENT_TIMESTAMP |
| updated_at    | DATETIME     | DEFAULT CURRENT_TIMESTAMP |

### Password Rules

Passwords must satisfy the following requirements:

* Minimum 8 characters
* At least 1 numeric character
* At least 1 uppercase character
* At least 1 lowercase character
* At least 1 special character

Password complexity will be validated in Python.

Only the password hash will be stored in the database.

Plain-text passwords must never be stored.

### Relationship

```
roles 1 ───── N users
```

---

## 5.3 Categories

The `categories` table stores product categories.

```text
categories
├── category_id
├── category_name
├── description
└── created_at
```

### Fields

| Field         | Type         | Constraints               |
| ------------- | ------------ | ------------------------- |
| category_id   | INT          | PK, AUTO_INCREMENT        |
| category_name | VARCHAR(100) | NOT NULL, UNIQUE          |
| description   | VARCHAR(255) | NULL                      |
| created_at    | DATETIME     | DEFAULT CURRENT_TIMESTAMP |

### Example Categories

* Electronics
* Clothing
* Books
* Home & Kitchen
* Beauty
* Sports

### Relationship

```text
categories 1 ───── N products
```

---

## 5.4 Products

The `products` table stores products available in the store.

```text
products
├── product_id
├── product_name
├── description
├── sku
├── price
├── stock_quantity
├── category_id
├── is_active
├── created_at
└── updated_at
```

### Fields

| Field          | Type          | Constraints               |
| -------------- | ------------- | ------------------------- |
| product_id     | INT           | PK, AUTO_INCREMENT        |
| product_name   | VARCHAR(150)  | NOT NULL                  |
| description    | TEXT          | NULL                      |
| sku            | VARCHAR(50)   | NOT NULL, UNIQUE          |
| price          | DECIMAL(10,2) | NOT NULL, >= 0            |
| stock_quantity | INT           | NOT NULL, >= 0            |
| category_id    | INT           | NOT NULL, FK              |
| is_active      | BOOLEAN       | DEFAULT TRUE              |
| created_at     | DATETIME      | DEFAULT CURRENT_TIMESTAMP |
| updated_at     | DATETIME      | DEFAULT CURRENT_TIMESTAMP |

### Important Decisions

`DECIMAL` will be used for product prices instead of `FLOAT` because prices require accurate decimal representation.

Stock quantity must never be negative.

Products will generally not be physically deleted after being used by orders.

Instead, `is_active` can be set to `FALSE`.

This allows historical orders to continue referencing products.

### Relationship

```
categories 1 ───── N products
```

---

## 5.5 Cart

The `cart` table represents a user's active shopping cart.

```
cart
├── cart_id
├── user_id
├── created_at
└── updated_at
```

### Fields

| Field      | Type     | Constraints               |
| ---------- | -------- | ------------------------- |
| cart_id    | INT      | PK, AUTO_INCREMENT        |
| user_id    | INT      | NOT NULL, UNIQUE, FK      |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### Business Rule

Each user has one active cart.

The `UNIQUE` constraint on `user_id` enforces:

```
One user → One active cart
```

### Relationship

```
users 1 ───── 1 cart
```

---

## 5.6 Cart Items

The `cart_items` table stores products currently present in a user's cart.

```
cart_items
├── cart_item_id
├── cart_id
├── product_id
├── quantity
└── added_at
```

### Fields

| Field        | Type     | Constraints               |
| ------------ | -------- | ------------------------- |
| cart_item_id | INT      | PK, AUTO_INCREMENT        |
| cart_id      | INT      | NOT NULL, FK              |
| product_id   | INT      | NOT NULL, FK              |
| quantity     | INT      | NOT NULL, > 0             |
| added_at     | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### Important Constraint

The combination of `cart_id` and `product_id` must be unique.

```
UNIQUE(cart_id, product_id)
```

This prevents the same product from appearing multiple times in the same cart.

Instead, the quantity should be updated.

### Stock Rule

Adding a product to a cart does **not** reduce stock.

Stock will be checked and reduced when an order is placed.

### Relationships

```
cart 1 ───── N cart_items

products 1 ───── N cart_items
```

`cart_items` resolves the many-to-many relationship between carts and products.

---

## 5.7 Orders

The `orders` table represents completed or in-progress purchases.

```
orders
├── order_id
├── user_id
├── order_status
├── total_amount
├── shipping_address
├── payment_method
├── payment_status
├── created_at
└── updated_at
```

### Fields

| Field            | Type          | Constraints               |
| ---------------- | ------------- | ------------------------- |
| order_id         | INT           | PK, AUTO_INCREMENT        |
| user_id          | INT           | NOT NULL, FK              |
| order_status     | VARCHAR(...)  | NOT NULL                  |
| total_amount     | DECIMAL(10,2) | NOT NULL, >= 0            |
| shipping_address | TEXT          | NOT NULL                  |
| payment_method   | VARCHAR(...)  | NOT NULL                  |
| payment_status   | VARCHAR(...)  | NOT NULL                  |
| created_at       | DATETIME      | DEFAULT CURRENT_TIMESTAMP |
| updated_at       | DATETIME      | DEFAULT CURRENT_TIMESTAMP |

### Order Statuses

The initial order lifecycle will be:

```
pending
   ↓
confirmed
   ↓
shipped
   ↓
delivered
```

An order can also become:

```
cancelled
```

The status system will remain intentionally simple for this project.

### Shipping Address

The shipping address will be stored directly on the order as a snapshot.

This means an old order retains the address used when the order was placed, even if the user changes their address later.

A separate address-management table is intentionally avoided to keep the project compact.

### Payment

No real payment gateway will be implemented initially.

The project will only track:

#### Payment Methods

* COD
* CARD
* UPI

#### Payment Statuses

* pending
* paid
* failed

Actual payment processing can be added in a future version.

### Relationship

```text
users 1 ───── N orders
```

A user can have multiple orders.

---

## 5.8 Order Items

The `order_items` table stores the products included in each order.

```
order_items
├── order_item_id
├── order_id
├── product_id
├── quantity
├── unit_price
└── subtotal
```

### Fields

| Field         | Type          | Constraints        |
| ------------- | ------------- | ------------------ |
| order_item_id | INT           | PK, AUTO_INCREMENT |
| order_id      | INT           | NOT NULL, FK       |
| product_id    | INT           | NOT NULL, FK       |
| quantity      | INT           | NOT NULL, > 0      |
| unit_price    | DECIMAL(10,2) | NOT NULL, >= 0     |
| subtotal      | DECIMAL(10,2) | NOT NULL, >= 0     |

### Price Snapshot

`unit_price` stores the product price at the time of purchase.

Example:

```
Product price when purchased = ₹1000

quantity = 2
unit_price = ₹1000
subtotal = ₹2000
```

If the product price later changes to ₹1200, the existing order must still retain the original ₹1000 price.

Therefore, order history does not depend on the current product price.

### Subtotal

```text
subtotal = quantity × unit_price
```

### Relationships

```
orders 1 ───── N order_items

products 1 ───── N order_items
```

---

# 6. Complete Database Relationships

```
roles
  │
  │ 1:N
  ▼
users
  │
  ├──────── 1:1 ──────── cart
  │                       │
  │                       │ 1:N
  │                       ▼
  │                  cart_items
  │                       │
  │                       │ N:1
  │                       ▼
  │                    products
  │                       ▲
  │                       │ N:1
  │                       │
  │                   categories
  │
  │ 1:N
  ▼
orders
  │
  │ 1:N
  ▼
order_items
  │
  │ N:1
  ▼
products
```

---

# 7. Database Constraints

The database will enforce important data-integrity rules.

### Primary Keys

Every table will have a primary key.

### Unique Constraints

The following values must be unique:

* `roles.role_name`
* `users.email`
* `users.phone`
* `categories.category_name`
* `products.sku`
* `cart.user_id`
* `(cart_items.cart_id, cart_items.product_id)`

### Foreign Keys

Foreign-key relationships will be used to maintain referential integrity.

### Value Constraints

The database should prevent invalid values such as:

```text
price < 0
stock_quantity < 0
quantity <= 0
total_amount < 0
unit_price < 0
subtotal < 0
```

---

# 8. Foreign Key Delete Strategy

Historical business data should not be accidentally deleted through cascading deletes.

Products used by historical orders should not be physically deleted.

Instead:

```
products.is_active = FALSE
```

will be used to deactivate products.

Foreign-key relationships will therefore be designed carefully rather than applying `ON DELETE CASCADE` everywhere.

---

# 9. Triggers

Triggers will be used selectively where database-level automation is useful.

## Planned Trigger 1 — User Timestamp

Automatically update:

```
users.updated_at
```

when a user record is modified.

## Planned Trigger 2 — Product Timestamp

Automatically update:

```
products.updated_at
```

when a product record is modified.

## Planned Trigger 3 — Cart Timestamp

Automatically update:

```
cart.updated_at
```

when cart data changes.

## Planned Trigger 4 — Order Timestamp

Automatically update:

```
orders.updated_at
```

when an order record is modified.

## Planned Trigger 5 — Order Item Subtotal

When an order item is inserted or updated:

```
subtotal = quantity × unit_price
```

can be maintained automatically.

### Stock Management Decision

Stock reduction will **not** be handled by a simple order-item trigger.

Instead, stock management will be handled inside a Python database transaction.

Reason:

```text
Check stock
    ↓
Create order
    ↓
Create order items
    ↓
Reduce stock
    ↓
Commit transaction
```

This provides better control over order placement and future cancellation/refund logic.

---

# 10. Views

Two useful database views are planned.

## 10.1 Active Products View

A view for retrieving active products.

It can include relevant category information and only expose products where:

```
is_active = TRUE
```

This will simplify product listing queries.

## 10.2 Order Summary View

A view combining order and related information for easier reporting.

Possible information:

* Order ID
* Customer
* Order status
* Number of items
* Total amount
* Order date

This will provide practice with:

* JOIN
* GROUP BY
* Aggregate functions

---

# 11. Seed Data

Initial seed data will be inserted for development and testing.

## Roles

```
customer
admin
```

## Categories

```
Electronics
Clothing
Books
Home & Kitchen
Beauty
Sports
```

## Example Products

```
Wireless Mouse
Mechanical Keyboard
T-Shirt
Running Shoes
Python Book
Water Bottle
```

The seed dataset will remain small and focused on development/testing.

---

# 12. Order Processing Flow

The expected order-placement flow is:

```
User
  ↓
Cart
  ↓
Cart Items
  ↓
Place Order
  ↓
Validate Cart
  ↓
Check Product Availability
  ↓
Check Stock
  ↓
Create Order
  ↓
Create Order Items
  ↓
Calculate / Store Order Total
  ↓
Reduce Product Stock
  ↓
Clear Cart
  ↓
Commit Transaction
```

If any critical step fails:

```
ROLLBACK
```

This prevents partially created orders.

---

# 13. Authentication

Authentication will be implemented in the Python backend.

### Registration

```
User Input
    ↓
Validate Input
    ↓
Validate Password Complexity
    ↓
Hash Password
    ↓
Store User
```

### Login

```
Email + Password
       ↓
Find User
       ↓
Verify Password Hash
       ↓
Authenticate User
```

Authorization will use the user's role.

Example:

```
customer → customer functionality
admin    → administrative functionality
```

---

# 14. Backend Components

The backend will eventually contain functionality for:

## User Management

* Registration
* Login
* User retrieval
* User updates
* Role-based authorization

## Category Management

* Create category
* Read categories
* Update category
* Deactivate/delete category where appropriate

## Product Management

* Create product
* Read products
* Update product
* Deactivate product
* Stock management

## Cart Management

* Create/retrieve cart
* Add product
* Update quantity
* Remove product
* View cart

## Order Management

* Place order
* View orders
* View order details
* Update order status
* Handle cancellation according to business rules

## Admin Functionality

* Manage products
* Manage categories
* View orders
* Update order status
* Manage inventory

---

# 15. Transaction Strategy

Database transactions will be used for operations that modify multiple related records.

The most important example is order placement.

```
BEGIN TRANSACTION

Check stock
Create order
Create order items
Update product stock
Clear cart

COMMIT
```

If an operation fails:

```
ROLLBACK
```

This prevents inconsistent states such as:

```
Order created
but
Stock not updated
```

---

# 16. Project Structure

The project structure will evolve as development progresses.

Current structure:

```
ShopSphere/
└── docs/
    └── architecture.md
```

Planned structure:

```text
ShopSphere/
├── docs/
│   └── architecture.md
├── database/
├── backend/
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

Files and folders will be added only when they are needed.

---

# 17. Development Approach

The project will follow this workflow:

```
Learn
  ↓
Design
  ↓
Implement
  ↓
Test
  ↓
Git Commit
  ↓
Next Feature
```

The objective is to understand each part rather than simply copying a completed project.

---

# 18. Development Timeline

The initial target is approximately 10 days with around 1–1.5 hours of work per day.

The timeline is flexible and may change depending on learning progress.

### Day 1

* Database planning
* Git setup
* Architecture documentation

### Day 2

* Create database tables
* Primary keys
* Foreign keys
* Constraints

### Day 3

* Triggers
* Views
* Seed data
* SQL testing

### Day 4

* Python setup
* PyMySQL
* Database connection
* Basic CRUD practice

### Day 5

* Categories
* Products
* Product CRUD

### Day 6

* Users
* Password hashing
* Registration
* Login
* Authorization

### Day 7

* Cart
* Cart items
* Cart operations

### Day 8

* Orders
* Order items
* Transactions
* Stock handling

### Day 9

* Admin functionality
* Validation
* Error handling

### Day 10

* Testing
* Documentation
* Cleanup
* Git/GitHub
* Final review

---

# 19. Current Status

Database design has been completed conceptually.

### Designed Tables

* `roles`
* `users`
* `categories`
* `products`
* `cart`
* `cart_items`
* `orders`
* `order_items`

### Designed Database Features

* Primary keys
* Foreign keys
* Unique constraints
* Value constraints
* Relationships
* Triggers
* Views
* Seed data
* Transactions
* Stock management strategy

### Current Phase

```text
Database Design
      ✓
      ↓
SQL Implementation
      ↓
Python + MySQL
      ↓
Backend Development
      ↓
Testing
```

The next implementation step is to create the MySQL database and begin writing the SQL schema.
