# ShopSphere — E-Commerce Backend

## 1. Project Overview

ShopSphere is a small e-commerce backend application designed for learning and demonstrating backend development using Python and MySQL.

The project will be developed incrementally and maintained using Git.

---

## 2. Project Goals

* Build a functional e-commerce backend
* Practice relational database design
* Use MySQL constraints, relationships, triggers, and views
* Connect Python to MySQL using PyMySQL
* Build backend APIs
* Implement customer and admin functionality
* Maintain the project using Git throughout development

---

## 3. Technology Stack

* Python
* MySQL
* PyMySQL
* FastAPI — to be introduced during backend development
* Git / GitHub

---

## 4. High-Level Architecture

```text
Client
   |
   v
Python Backend
   |
   v
PyMySQL
   |
   v
MySQL Database
```

The database will contain the core business data, while Python will handle application logic, validation, authentication, and API functionality.

---

# 5. Database Architecture

## 5.1 Roles

The `roles` table stores the roles available in the system.

### Current Roles

* `customer`
* `admin`

```text
roles
├── role_id
└── role_name
```

### Relationship

```text
roles 1 ──────────< users
```

One role can be assigned to many users.

---

## 5.2 Users

The `users` table stores customer and administrator accounts.

```text
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

### Constraints

* `user_id` — Primary Key, Auto Increment
* `first_name` — NOT NULL
* `last_name` — NOT NULL
* `email` — UNIQUE, NOT NULL
* `password_hash` — NOT NULL
* `phone` — UNIQUE, NOT NULL
* `dob` — NOT NULL
* `role_id` — Foreign Key referencing `roles.role_id`
* `created_at` — automatically stores account creation time
* `updated_at` — tracks the latest modification

### Design Decisions

* Passwords will not be stored directly.
* The backend will validate password complexity.
* The backend will hash passwords before storing them.
* Phone numbers will be stored as `VARCHAR`, not a numeric data type.
* `dob` is stored instead of `age` because age is derived data and changes over time.
* New registrations will default to the `customer` role.
* Admin privileges will not be assigned through normal customer registration.
* `updated_at` will eventually be maintained automatically.

---

## 5.3 Categories

The `categories` table groups products into logical categories.

```text
categories
├── category_id
├── category_name
├── description
└── created_at
```

### Constraints

* `category_id` — Primary Key, Auto Increment
* `category_name` — UNIQUE, NOT NULL
* `description` — Optional
* `created_at` — automatically stores creation time

### Example Categories

```text
Electronics
Clothing
Books
Home & Kitchen
Beauty
Sports
```

### Relationship

```text
categories 1 ──────────< products
```

One category can contain many products.

---

## 5.4 Products

The `products` table stores the products available in the store.

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

### Constraints

* `product_id` — Primary Key, Auto Increment
* `product_name` — NOT NULL
* `description` — Optional
* `sku` — UNIQUE, NOT NULL
* `price` — NOT NULL
* `stock_quantity` — NOT NULL and must not be negative
* `category_id` — Foreign Key referencing `categories.category_id`
* `is_active` — defaults to TRUE
* `created_at` — automatically stores creation time
* `updated_at` — tracks the latest modification

### Design Decisions

#### Price

`DECIMAL(10,2)` will be used for product prices because monetary values require exact decimal precision.

We will not use `FLOAT` for prices.

#### SKU

SKU stands for **Stock Keeping Unit**.

Each product will have a unique SKU.

Example:

```text
IPH15-BLK-128
TSHIRT-BLU-M
SONY-WH1000XM5
```

#### Stock

`stock_quantity` represents the number of units currently available.

Negative stock will not be allowed.

#### Active Products

Products will have an `is_active` flag.

Instead of deleting a product that is no longer sold:

```text
is_active = FALSE
```

This allows historical orders to continue referencing the product.

---

# 6. Current Entity Relationship Overview

```text
                    ┌──────────────┐
                    │    roles     │
                    ├──────────────┤
                    │ role_id  PK  │
                    │ role_name    │
                    └──────┬───────┘
                           │
                           │ 1:N
                           │
                    ┌──────▼───────┐
                    │    users     │
                    ├──────────────┤
                    │ user_id  PK  │
                    │ role_id  FK  │
                    │ first_name   │
                    │ last_name    │
                    │ email        │
                    │ password_hash│
                    │ phone        │
                    │ dob          │
                    │ created_at   │
                    │ updated_at   │
                    └──────────────┘


                    ┌──────────────┐
                    │  categories  │
                    ├──────────────┤
                    │ category_id  │
                    │ category_name│
                    │ description  │
                    │ created_at   │
                    └──────┬───────┘
                           │
                           │ 1:N
                           │
                    ┌──────▼───────┐
                    │   products   │
                    ├──────────────┤
                    │ product_id   │
                    │ category_id  │
                    │ product_name │
                    │ description  │
                    │ sku          │
                    │ price        │
                    │ stock        │
                    │ is_active    │
                    │ created_at   │
                    │ updated_at   │
                    └──────────────┘
```

---

# 7. Development Approach

The project will be developed incrementally.

New folders and files will be created only when they become necessary.

Git will be used throughout development to track meaningful changes.

```text
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

---

# 8. Planned Database Components

The database will eventually include:

* Tables
* Primary Keys
* Foreign Keys
* Unique Constraints
* Check Constraints
* Indexes
* Triggers
* Views
* Seed / Sample Data

Only components that provide meaningful functionality or learning value will be added.

---

# 9. Planned Backend Components

## Customer

* Registration
* Login
* Browse products
* Search products
* View product details
* Add products to cart
* Update cart
* Remove cart items
* Place orders
* View order history

## Admin

* Manage products
* Manage categories
* View orders
* Update order status
* Manage store inventory

---

# 10. Project Structure

The project structure will evolve as development progresses.

Files and folders will be created only when they are required.

Current structure:

```text
ShopSphere/
│
└── docs/
    └── architecture.md
```

Planned structure:

```text
ShopSphere/
│
├── docs/
│
├── database/
│
├── backend/
│
├── tests/
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 11. Current Status

## Database Design

* [x] Roles table — designed
* [x] Users table — designed
* [x] Categories table — designed
* [x] Products table — designed
* [ ] Cart
* [ ] Cart Items
* [ ] Orders
* [ ] Order Items
* [ ] Additional tables if required

## Database Implementation

* [ ] Schema
* [ ] Constraints
* [ ] Indexes
* [ ] Triggers
* [ ] Views
* [ ] Seed Data

## Backend

* [ ] Python project setup
* [ ] PyMySQL connection
* [ ] Database access layer
* [ ] API structure
* [ ] Authentication
* [ ] Product APIs
* [ ] Cart APIs
* [ ] Order APIs
* [ ] Admin APIs

## Documentation

* [x] Initial architecture document
* [ ] Database documentation
* [ ] API documentation
* [ ] Final README

---

# 12. Development Timeline

Target completion time: **10 days**

Approximately **1–1.5 hours per day**.

| Day    | Goal                                 |
| ------ | ------------------------------------ |
| Day 1  | Database planning + Git setup        |
| Day 2  | Tables + relationships + constraints |
| Day 3  | Triggers + views + seed data         |
| Day 4  | Python + PyMySQL connection          |
| Day 5  | Products + categories backend        |
| Day 6  | Users + authentication               |
| Day 7  | Cart                                 |
| Day 8  | Orders                               |
| Day 9  | Admin + validation + error handling  |
| Day 10 | Testing + documentation + cleanup    |

The timeline is flexible. Understanding the project is more important than strictly completing a task on a particular day.
