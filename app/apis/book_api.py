from fastapi import APIRouter, HTTPException, Query, status
from app.configuration.exceptions import DBException, LlmException
from app.db.Adapter import BookAdapter
from app.db.domains.BookRepository import BookRepository
from app.schemas.bookSchema import BookRecommendation, BookSchema, BookCreateSchema
from app.utils.LlmProvider import llm_provider
from app.utils.LoggerProvider import logger
from app.models.Book import BookModel
from app.configuration.responses import (
    post_responses,
    get_response,
    get_responses,
    delete_response,
)

router = APIRouter()
book_repository: BookRepository = BookRepository()
adapter: BookAdapter = BookAdapter()


class BookApiRouter:
    # Endpoint to create a new book
    @router.post(
        "/books/",
        response_model=BookSchema,
        status_code=status.HTTP_201_CREATED,
        responses=post_responses,
    )
    async def create_book(
        book: BookCreateSchema,
    ):
        """
        Create a new book.

        - **book**: Details of the book to create.
        """
        try:
            logger.info("Creating new Book")
            db_book: BookModel = llm_provider.generate_book_info(book)
        except LlmException as exc:
            logger.error(f"Error creating book: {exc}")
            raise HTTPException(status_code=500, detail=str(exc))
        try:
            book = book_repository.create(db_book=db_book)
        except DBException as exc:
            logger.error(f"Error creating book: {exc}")
            raise HTTPException(status_code=500, detail=str(exc))
        return book

    @router.get(
        "/books/recommendation",
        response_model=list[BookRecommendation],
        responses=get_responses,
    )
    async def get_recommendation(
        offset: int = Query(0, ge=0),
        limit: int = Query(10, gt=0),
    ) -> list[BookRecommendation]:
        """
        Get recommendations for a book by books in the DB.

        - **offset**: Offset for pagination (default: 0).
        - **limit**: Limit of books per page (default: 10).
        """
        logger.info("Creating reccomendations")
        books: list[BookModel] = book_repository.find_all(offset=offset, limit=limit)
        reccomendation_books: list[BookModel] = llm_provider.generate_reccomendations(
            books
        )
        b = [adapter.to_data_source(book) for book in reccomendation_books]
        return b

    # Endpoint to get book by id
    @router.get(
        "/books/{book_id}",
        response_model=BookSchema,
        responses=get_response,
    )
    async def get_book(book_id) -> BookSchema:
        """
        Get a book by its ID.

        - **book_id**: ID of the book to fetch.
        """
        logger.info("Reading a book")
        book = book_repository.find_one(book_id=book_id)
        if book is None:
            logger.error(f"Error while getting a book")
            raise HTTPException(status_code=404, detail="Book is not found")
        return book

    @router.delete(
        "/books/{book_id}",
        status_code=204,
        responses=delete_response,
    )
    async def delete_book(book_id: str) -> None:
        """
        Delete a book by its ID.

        - **book_id**: ID of the book to delete.
        """

        logger.info("Reading a book")
        del_count: int = book_repository.delete_one(book_id=book_id)
        if del_count == 0:
            logger.error(f"Error while deleting a book")
            raise HTTPException(status_code=404, detail="Book is not found")

    # Endpoint to get all books
    @router.get("/books/", response_model=list[BookSchema], responses=get_responses)
    async def get_books(
        offset: int = Query(0, ge=0),
        limit: int = Query(10, gt=0),
    ) -> list[BookSchema]:
        """
        Get all books.

        - **offset**: Offset for pagination (default: 0).
        - **limit**: Limit of books per page (default: 10).
        """
        logger.info("Reading books")
        return book_repository.find_all(offset=offset, limit=limit)
