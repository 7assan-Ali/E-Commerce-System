# 🛒 E-Commerce System

A Python-based **Object-Oriented E-Commerce System** designed from a UML class model and implemented with a desktop GUI using **Tkinter**.

The project demonstrates core OOP concepts such as **inheritance, composition, association, encapsulation, and object collaboration** through a complete shopping workflow.

## ✨ Features

### 🔐 Authentication
- Customer Login
- Admin Login
- Customer Sign Up
- Password fields are hidden in the GUI
- Logout

### 👤 Customer
- Browse products
- View product prices and stock
- Add products to cart
- Update cart quantities
- Remove items from cart
- Calculate cart total
- Checkout
- Create orders
- View and cancel orders when allowed
- View and update profile
- Manage address
- Add, update, and delete reviews

### 👨‍💼 Admin
- Admin dashboard
- Add products
- Update product price
- Update product stock
- Delete products
- Manage orders
- Update order status
- Manage shipments
- View admin profile

### 💳 Order & Payment Flow
The system models the main e-commerce workflow:

`Customer → Cart → CartItem → Order → OrderItem → Payment → Shipment`

## 🧩 OOP Design

The main classes are organized inside `src/models/`:

| Class | Responsibility |
|---|---|
| `User` | Base user information and authentication |
| `Customer` | Customer-specific operations |
| `Admin` | Product and order management |
| `Product` | Product information, price and stock |
| `Cart` | Shopping cart management |
| `CartItem` | Product quantity and subtotal |
| `Order` | Customer order and status |
| `OrderItem` | Products inside an order |
| `Payment` | Payment processing and refund |
| `Address` | Customer shipping address |
| `Review` | Product review management |
| `Shipment` | Shipping and tracking status |

### Inheritance

```text
User
├── Customer
└── Admin
```

`Customer` and `Admin` inherit common authentication and profile functionality from `User`.

## 📁 Project Structure

```text
E-Commerce-System/
│
├── src/
│   ├── main.py
│   │
│   ├── gui/
│   │   └── app.py
│   │
│   └── models/
│       ├── user.py
│       ├── customer.py
│       ├── admin.py
│       ├── product.py
│       ├── category.py
│       ├── cart.py
│       ├── cart_item.py
│       ├── order.py
│       ├── order_item.py
│       ├── payment.py
│       ├── address.py
│       ├── review.py
│       └── shipment.py
│
├── tests/
├── README.md
└── requirements.txt
```

## 🖥️ GUI

The desktop application is implemented using **Tkinter**.

The GUI provides separate interfaces for:

- Customer
- Admin
- Login
- Sign Up
- Product catalog
- Shopping cart
- Orders
- Payments
- Shipments
- Profile management

## 🛍️ Product Catalog

The application starts with sample products such as:

| Product | Price (EGP) | Stock |
|---|---:|---:|
| Dell Laptop | 45,000 | 10 |
| iPhone 15 | 38,000 | 8 |
| Samsung Galaxy S24 | 32,000 | 12 |
| AirPods Pro | 9,500 | 20 |
| Logitech Mouse | 1,500 | 25 |
| Mechanical Keyboard | 3,000 | 15 |
| HP Monitor 24 inch | 7,500 | 10 |
| USB-C Hub | 1,200 | 30 |

## ⚙️ Technologies

- **Python 3**
- **Object-Oriented Programming (OOP)**
- **Tkinter**
- Git & GitHub

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/7assan-Ali/E-Commerce-System.git
cd E-Commerce-System
```

### 2. Run the application

```bash
python src/main.py
```

## 🔄 Main Application Flow

```text
Start Application
       │
       ▼
     Login
       │
   ┌───┴────┐
   ▼        ▼
Customer   Admin
   │        │
   ▼        ▼
Products  Products
   │        │
   ▼        ├── Add
  Cart      ├── Update
   │        └── Delete
   ▼
Checkout
   │
   ▼
 Order
   │
   ├── Payment
   │
   └── Shipment
```

## 🎯 Project Goals

- Apply Object-Oriented Programming principles in a practical project.
- Convert a UML class design into Python classes.
- Build a functional desktop e-commerce interface.
- Demonstrate relationships between multiple domain objects.
- Practice GitHub-based project organization and version control.

## 👨‍💻 Author

**Hassan Ali**

GitHub: https://github.com/7assan-Ali

---

⭐ If you find this project useful, feel free to star the repository.
