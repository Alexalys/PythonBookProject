from sqlalchemy.orm import Session
from app.db.BaseRepository import BaseRepository
from app.db.database import get_session
from app.models.Book import BookModel


class BookRepository(BaseRepository):
    def create(self, db_book: BookModel):
        with get_session() as db:
            db.add(db_book)
            db.commit()
            db.refresh(db_book)
            return db_book

    def find_one(self, book_id: int):
        with get_session() as db:
            return db.query(BookModel).filter(BookModel.uuid == book_id).first()

    def find_all(self, offset: int = 0, limit: int = 10):
        with get_session() as db:
            return db.query(BookModel).offset(offset).limit(limit).all()
