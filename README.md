ShopSphere — E-Commerce Backend System
ShopSphere is a backend-focused e-commerce project built with Python and MySQL. It implements core shopping workflows—from managing users and products to maintaining carts and placing orders—using Python business logic and a relational database.

The project emphasizes database integrity, input validation, stock management, and automated testing. It is not a web application: there is no frontend or FastAPI layer.
Tech Stack
- Language: Python
- Database: MySQL
- Database connectivity: PyMySQL
- Testing: pytest
- Version control: Git and GitHub
Core Features
Module	Capabilities
Users	Registration, password validation and hashing, role-based records, profile operations, account activation/deactivation
Categories	Create, read, update, and delete categories
Products	Product management, deactivation, and stock handling
Cart	Add, update, and remove items; view contents and calculate totals
Orders	Create orders from carts, verify stock, reduce inventory, create order items, calculate totals, clear carts after successful orders, and update order/payment statuses


Architecture
Python backend modules
         |
       PyMySQL
         |
         v
    MySQL database
Python handles application logic and communicates directly with MySQL through PyMySQL.
Database Design
The relational database models these entities:

roles · users · categories · products · cart · cart_items · orders · order_items

The schema uses primary and foreign keys, unique and check constraints, defaults, and transactions to support data integrity. It also includes:
- Triggers for update timestamps and order-item subtotal calculations.
- Views such as active_products_view and order_summary_view for commonly needed queries.
Order Processing Workflow
1. Read the customer's cart items.
2. Check product availability and stock.
3. Create the order and its order-item records.
4. Update inventory and calculate the order total.
5. Clear the cart after successful order creation.
These steps are implemented in the Python backend with MySQL persistence.
Automated Testing
The project includes a pytest suite covering:
- User operations and validation
- Categories and products
- Cart functionality
- Order processing
Documented test result: 48 passed

To run the tests from the repository root after configuring the project dependencies and database environment:
pytest
The test count above reflects the project's documented result; it is not a live CI status badge.

Repository Structure
ShopSphere/
├── backend/          # Python database connection and business logic
├── docs/             # Project documentation
├── tests/            # pytest test suite
├── requirements.txt  # Python dependencies
├── .gitignore
└── README.md
Project Scope and Status
Status: Core implementation completed.

ShopSphere is a Python + MySQL backend learning project designed to demonstrate relational database modeling, practical business logic, validation, and automated testing. It intentionally does not include a frontend, REST API, or FastAPI framework.
Key Skills Demonstrated
Python · SQL · MySQL · PyMySQL · Relational Database Design · Transactions · Input Validation · Business Logic · pytest · Git
