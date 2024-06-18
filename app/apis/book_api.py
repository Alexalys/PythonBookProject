from fastapi import APIRouter, Depends, Query
from app.db.Repository import Repository
from app.db.database import SessionLocal
from app.schemas.bookSchema import Book, BookCreate
from app.utils.LlmProvider import LlmProvider
from app.utils.LoggerProvider import LoggerProvider
from sqlalchemy.orm import Session
from app.models.Book import BookModel
import datetime

router = APIRouter()
logger = LoggerProvider().get_logger()
repository = Repository()
llmProvier = LlmProvider()


# Dependency to get a SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class BookApiRouter:
    @router.get("/")
    async def root():
        logger.debug("Accessing /")

        return {"message": "Hello"}

    # Endpoint to create a new book
    @router.post("/books/", response_model=Book)
    async def create_book(book: BookCreate, db: Session = Depends(get_db)):
        db_book: BookModel = llmProvier.generate_book_info(book)
        return repository.create_book(db=db, db_book=db_book)

    # Endpoint to get book by id
    @router.get("/books/{book_id}", response_model=Book)
    async def get_book(book_id, db: Session = Depends(get_db)):
        return repository.get_book(db=db, book_id=book_id)

    # Endpoint to get all books
    @router.get("/books/", response_model=list[Book])
    async def get_book(
        offset: int = Query(0, ge=0),
        limit: int = Query(10, gt=0),
        db: Session = Depends(get_db),
    ):
        return repository.get_books(db=db, offset=offset, limit=limit)
