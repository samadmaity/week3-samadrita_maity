## Online Shopping Application API
A FastAPI backend for an online shopping application using PostgreSQL, SQLAlchemy, Pydantic, JWT authentication, role-based authorization, logging, background tasks, and router testing.

## Features

User registration and JWT login
Customer and admin role support
Product and category management
Product search and browsing
Cart management with stock validation
Order checkout and order history
Product stock reduction after checkout
Background order-confirmation task
Application logging in app.log
Swagger/OpenAPI documentation
Automated router tests using Pytest

## Technology Stack               TechnologyPurpose

      Python 3.12                Programming language


       FastAPI                      Web framework


     SQLAlchemy                 ORM and database access


     PostgreSQL                        Database


      PydantiC                Request and response validation


     JWT/OAuth2                      Authentication


       Pytest                       Automated testing


      Uvicorn                       Application server



## Architecture

Plain textSwagger UI
    ↓
Routers
    ↓
Services
    ↓
Repositories
    ↓
SQLAlchemy Models
    ↓
PostgreSQL


## Routers: Define API endpoints.
## Services: Contain business logic and validations.
## Repositories: Execute database operations.
## Models: Represent database tables.
## Schemas: Validate request and response data.
## Utils: Provide authentication, logging, helpers, and notifications.

## Project Structure

CASESTUDY-WEEK2/
├── app/
│   ├── models/
│   ├── database.py
│   └── main.py
├── repositories/
├── routers/
├── schemas/
├── services/
├── utils/
├── test/
│   ├── routes/
│   │   ├── test_user_router.py
│   │   ├── test_product_router.py
│   │   ├── test_cart_router.py
│   │   └── test_order_router.py
│   ├── conftest.py
│   └── testconfig.py
├── app.log
├── config.env
├── requirements.txt
└── README.md

## Main Endpoints
## Users

POST /users/register
POST /auth/login

## Products

GET /products/
GET /products/{product_id}
GET /products/search
POST /products/ — Admin only
PUT /products/{product_id} — Admin only
DELETE /products/{product_id} — Admin only

## Cart

POST /cart/add
GET /cart/{user_id}
PUT /cart/update/{cart_item_id}
DELETE /cart/remove/{cart_item_id}
GET /cart/{user_id}/summary

## Orders

POST /orders/checkout
GET /orders/{user_id}
GET /orders/details/{order_id}

## Validation and Security

Email format validation
Minimum password length
Numeric mobile validation
Duplicate email and product checks
Product stock validation
JWT-protected routes
Cart and order ownership checks
Admin-only product operations
Supported payment methods: card, cash, and upi

Passwords are hashed before storage and are never returned in API responses.
Running the Application

## Create a PostgreSQL database.
Configure the database URL and JWT settings in config.env.
Install dependencies:

Plain textpip install -r requirements.txt


## Start the application:

Plain textuvicorn app.main:app --reload


## Open Swagger UI:

Plain texthttp://127.0.0.1:8000/docs

## Testing
The project contains router tests for users, products, carts, and orders.
Run all router tests:
Plain textpython -m pytest test/routes -v

## Run coverage:
Plain textpython -m pytest test/routes --cov=routers --cov-report=term-missing

The tests cover successful requests, validation errors, authentication, authorization, cart ownership, checkout, stock reduction, and order history.
Logging and Background Tasks
Application logs are written to app.log.
After successful checkout, a background task runs an order-confirmation process without delaying the main API response.

## Project Status

## Completed:

PostgreSQL database integration
Layered FastAPI architecture
User, product, cart, and order modules
JWT authentication
Role-based authorization
Logging
Background tasks
Router-level automated tests