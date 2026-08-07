## Online Shopping Application API
A backend API for  online shopping application, built with FastAPI, SQLAlchemy, PostgreSQL, Pydantic, and a layered architecture.

## Features

User registration and login
Category and product management
Product browsing and search
Shopping cart management
Cart quantity and stock validation
Order checkout and order history
Product stock reduction after checkout
PostgreSQL database integration
Swagger/OpenAPI testing
Docker and Docker Compose support

## Technology Stack

| Technology | Purpose |

|---|---|

| Python 3.12 | Programming language |

| FastAPI | Backend web framework |

| SQLAlchemy | ORM and database interaction |

| PostgreSQL | Relational database |

| Pydantic | Request and response validation |

| Uvicorn | Application server |

| Docker | Application containerization |

| Docker Compose | Running the application and PostgreSQL together |

| Swagger/OpenAPI | API documentation and testing |

## Architecture

The application follows this request flow:
Client or Swagger UI → Router → Service → Repository → SQLAlchemy Model → PostgreSQL

Router Layer: Defines API endpoints and handles HTTP requests.
Service Layer: Contains business logic and validations.
Repository Layer: Executes database queries and CRUD operations.
Model Layer: Represents PostgreSQL database tables.
Schema Layer: Validates request and response data.
Utility Layer: Contains reusable helpers and exceptions.

## Project Structure

app/database.py – PostgreSQL connection and database sessions
app/models/ – User, category, product, cart, and order models
schemas/ – Pydantic request and response schemas
repositories/ – Database-access methods
services/ – Business logic
routers/ – API endpoints
utils/ – Helpers and reusable exceptions
tests/ – Automated tests
main.py – FastAPI application entry point

## Main API Endpoints

POST /users/register
POST /users/login
GET /categories/
POST /products/
GET /products/
GET /products/search
POST /cart/add
GET /cart/{user_id}
PUT /cart/update/{cart_item_id}
DELETE /cart/remove/{cart_item_id}
POST /orders/checkout
GET /orders/{user_id}
GET /orders/details/{order_id}

## Setup

Create a PostgreSQL database named Shopping, configure the database connection, install the required dependencies, and start the application using Uvicorn.
Swagger UI is available at:
/docs
For Docker execution, start the application using Docker Compose.
Testing Sequence

Register a user.
Log in.
Create or verify a category.
Create a product.
Add the product to the cart.
View or update the cart.
Complete checkout.
View order history and order details.

## Future Improvements

Password hashing
JWT authentication
Authorization checks
Alembic migrations
Automated tests
Pagination and caching
Payment integration
Administrator features



Add installation commands to this README
Create an ER diagram section for the README




