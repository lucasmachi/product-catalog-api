# Product Catalog REST API

A RESTful API for managing a product catalog, built with **FastAPI** and **SQLAlchemy**, with data persistence in a **SQLite** database.

##  Features

- Full CRUD for products (create, list, update, delete)
- Input data validation with **Pydantic**
- Result pagination for query optimization
- **HTTP Basic** authentication to protect routes
- Standardized error handling via `HTTPException`

## 🛠️Tech stack

- [Python 3.12+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [SQLite](https://www.sqlite.org/)
- [Poetry](https://python-poetry.org/) (dependency management)
- [Uvicorn](https://www.uvicorn.org/) (ASGI server)

## Project structure

```
.
├── main.py              # FastAPI app, models and routes
├── products.db           # SQLite database (auto-generated)
├── pyproject.toml       # Project dependencies (Poetry)
└── README.md
```

##  Getting started

### Prerequisites

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/docs/#installation) installed

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/lucasmachi/product-catalog-api.git
   cd repository-name
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Run the application:
   ```bash
   poetry run uvicorn main:app --reload
   ```

4. Access the interactive API docs (Swagger):
   ```
   http://127.0.0.1:8000/docs
   ```

## 🔐 Authentication

API routes are protected with **HTTP Basic Auth**. Use the credentials configured in the project to access the endpoints (username and password set in `main.py`).

##  Endpoints

| Method | Route              | Description                              |
|--------|---------------------|-------------------------------------------|
| GET    | `/products`         | Lists products with pagination (`page`, `limit`) |
| POST   | `/products`         | Adds a new product                        |
| PUT    | `/products/{id}`    | Updates an existing product                |
| DELETE | `/products/{id}`    | Removes a product                          |

### Example request body (POST)

```json
{
  "product_name": "Gaming Laptop",
  "product_category": "Electronics",
  "product_price": 4599.90
}
```


## 👤 Author

Developed by **Lucas Machi** as part of a Backend Development course (EBAC).
