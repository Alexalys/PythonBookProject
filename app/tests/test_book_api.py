import os
import pytest
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI
from httpx import AsyncClient

from unittest.mock import patch
from app.db.database import init_db, get_session
from app.models.Book import BookModel
from app.utils.LlmProvider import LlmProvider
from app.apis.book_api import router as book_router


app = FastAPI()
app.include_router(book_router)


@pytest.fixture(scope="module")
def test_db():
    # Initialize the database
    load_dotenv()
    db_url = os.getenv("TEST_DB_URL")
    init_db(db_url)
    # Create a new session
    with get_session() as session:
        # Create test data
        book = BookModel(
            uuid="123e4567-e89b-12d3-a456-426614174000",
            title="Test Book",
            author="Test Author",
            publication_date=datetime.strptime("2023-01-01", "%Y-%m-%d").date(),
            description="Test description",
            genre="Test genre",
        )
        session.add(book)
        session.commit()
        yield session
        # Teardown - remove test data
        try:
            session.query(BookModel).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e


# Mock the llm_provider methods
@pytest.fixture(scope="module")
def mock_llm_provider():
    with patch.object(
        LlmProvider, "generate_book_info"
    ) as mock_generate_book_info, patch.object(
        LlmProvider, "generate_reccomendations"
    ) as mock_generate_reccomendations:
        mock_generate_book_info.return_value = BookModel(
            title="Mocked Book",
            author="Mocked Author",
            publication_date=datetime.strptime("2023-01-01", "%Y-%m-%d").date(),
            description="Mocked description",
            genre="Mocked genre",
        )
        mock_generate_reccomendations.return_value = [
            BookModel(
                uuid="123e4567-e89b-12d3-a456-426614174001",
                title="Recommended Book",
                author="Recommended Author",
                publication_date=datetime.strptime("2023-01-01", "%Y-%m-%d").date(),
                description="Recommended description",
                genre="Recommended genre",
            )
        ]
        yield


@pytest.mark.usefixtures("test_db", "mock_llm_provider")
class TestBookAPI:

    async def test_create_book(self):
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.post(
                "/books/",
                json={
                    "title": "New Book",
                    "author": "New Author",
                    "publication_date": "2023-01-01",
                    "description": "New description",
                    "genre": "New genre",
                },
            )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Mocked Book"
        assert data["author"] == "Mocked Author"

    async def test_get_book(self):
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get("/books/123e4567-e89b-12d3-a456-426614174000")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Book"
        assert data["author"] == "Test Author"

    async def test_get_recommendation(self):
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get("/books/recommendation?offset=0&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Recommended Book"

    async def test_delete_book(self):
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.delete(
                "/books/123e4567-e89b-12d3-a456-426614174000"
            )
        assert response.status_code == 204
        async with AsyncClient(app=app, base_url="http://testserver") as client:
            response = await client.get("/books/123e4567-e89b-12d3-a456-426614174000")
        assert response.status_code == 404
