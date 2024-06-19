from fastapi import APIRouter, Query
from app.db.domains.BookRepository import BookRepository
from app.schemas.bookSchema import Book, BookCreate
from app.utils.LlmProvider import llm_provider
from app.utils.LoggerProvider import logger
from app.models.Book import BookModel

router = APIRouter()
book_repository: BookRepository = BookRepository()


class BookApiRouter:
    @router.get("/")
    async def root():
        logger.debug("Accessing /")

        return {"message": "Hello"}

    # Endpoint to create a new book
    @router.post("/books/", response_model=Book)
    async def create_book(book: BookCreate):
        db_book: BookModel = llm_provider.generate_book_info(book)
        return book_repository.create(db_book=db_book)

    # Endpoint to get book by id
    @router.get("/books/{book_id}", response_model=Book)
    async def get_book(book_id):
        return book_repository.find_one(book_id=book_id)

    # Endpoint to get all books
    @router.get("/books/", response_model=list[Book])
    async def get_book(
        offset: int = Query(0, ge=0),
        limit: int = Query(10, gt=0),
    ):
        return book_repository.find_all(offset=offset, limit=limit)
