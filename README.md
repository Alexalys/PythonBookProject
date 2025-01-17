
---

# Book Preference Management API

This project provides an API for managing book preferences using **FastAPI** and **PostgreSQL**. It integrates with the **ChatGPT API** to help generate book descriptions and receive recommendations. The API allows users to create a catalog of books, manage (CRUD operations) book entries, and get book recommendations based on previously read books.

---

## Features

- **Book Catalog Management**: Create, Read, Update, Delete (CRUD) operations on book entries.
- **Book Description Generation**: Automatically generate book descriptions using the OpenAI API (ChatGPT).
- **Book Recommendations**: Receive personalized book recommendations based on your previously read books.
- **FastAPI**: Fast and modern web framework for building APIs.
- **PostgreSQL**: Relational database for storing book data and preferences.

---

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **AI Integration**: OpenAI API (ChatGPT)
- **ORM**: SQLAlchemy
- **API Documentation**: FastAPI's interactive docs (Swagger UI)

---

## Installation

### Prerequisites

- **Python 3.7+** (preferably 3.8+)
- **PostgreSQL** (local or remote database)
- **OpenAI API Key** (for ChatGPT integration)

### 1. Clone the Repository

### 2. Create a Virtual Environment and Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Up the Database

- Ensure that you have **PostgreSQL** installed and running.
- Create a new PostgreSQL database:

```bash
psql -U postgres
CREATE DATABASE book_preference_db;
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root directory and add the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost/book_preference_db
OPENAI_API_KEY=your-openai-api-key
```

- Replace `username` and `password` with your PostgreSQL credentials.
- Get your **OpenAI API Key** from [OpenAI's official website](https://platform.openai.com/signup).

### 5. Database Migrations

Apply the database migrations using Alembic to set up the schema:

```bash
alembic upgrade head
```

---

## Running the Application

To run the FastAPI application, use `uvicorn`:

```bash
python3 main.py
```

- Open your browser and navigate to [http://localhost:8000](http://localhost:8000).
- FastAPI automatically generates interactive API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## API Endpoints

### 1. **Create Book**

- **Endpoint**: `POST /books/`
- **Description**: Add a new book to the catalog. Optionally, provide a description or let the system generate it via OpenAI.
- **Request Body**:
  ```json
  {
    "title": "Book Title",
    "author": "Book Author",
    "genre": "Book Genre",
    "description": "Description of the book (optional)"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Book Title",
    "author": "Book Author",
    "genre": "Book Genre",
    "description": "Generated or provided book description"
  }
  ```

### 2. **Get Book by ID**

- **Endpoint**: `GET /books/{book_id}/`
- **Description**: Retrieve details of a specific book by its ID.
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Book Title",
    "author": "Book Author",
    "genre": "Book Genre",
    "description": "Book Description"
  }
  ```

### 3. **Update Book**

- **Endpoint**: `PUT /books/{book_id}/`
- **Description**: Update the details of a specific book.
- **Request Body**:
  ```json
  {
    "title": "Updated Book Title",
    "author": "Updated Author",
    "genre": "Updated Genre",
    "description": "Updated Description"
  }
  ```

### 4. **Delete Book**

- **Endpoint**: `DELETE /books/{book_id}/`
- **Description**: Delete a book from the catalog by its ID.
- **Response**:
  ```json
  {
    "message": "Book deleted successfully"
  }
  ```

### 5. **Get Book Recommendations**

- **Endpoint**: `GET /recommendation/`
- **Description**: Get a list of recommended books based on previously read books. The recommendations are personalized based on the books you’ve read.
- **Response**:
  ```json
  [
    {
      "id": 2,
      "title": "Recommended Book 1",
      "author": "Author 1",
      "genre": "Genre 1",
      "description": "Book description"
    },
    {
      "id": 3,
      "title": "Recommended Book 2",
      "author": "Author 2",
      "genre": "Genre 2",
      "description": "Book description"
    }
  ]
  ```

---

## How ChatGPT Integration Works

When adding a new book to the catalog, you can either provide a description directly, or if you leave the description blank, the system will automatically call the OpenAI API to generate a description for the book. This is done using the **ChatGPT** model to generate a creative, contextually accurate description based on the book's title and author.

---

## Testing

To test the API, you can use tools like **Postman** or **curl**, or simply use the interactive API documentation provided by FastAPI.

Example with `curl`:

1. **Create a Book**:
   ```bash
   curl -X 'POST' 'http://localhost:8000/books/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{
     "title": "The Great Gatsby",
     "author": "F. Scott Fitzgerald",
     "genre": "Fiction"
   }'
   ```

2. **Get Recommendations**:
   ```bash
   curl -X 'GET' 'http://localhost:8000/recommendation/' -H 'accept: application/json'
   ```

---

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add feature'`).
5. Push to your branch (`git push origin feature/your-feature`).
6. Create a new pull request.

---
