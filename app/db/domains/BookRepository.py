from sqlalchemy.exc import IntegrityError
from app.configuration.exceptions import DBException
from app.db.BaseRepository import BaseRepository
from app.db.database import get_session
from app.models.Book import BookModel


class BookRepository(BaseRepository):
    def create(self, db_book: BookModel):
        try:
            with get_session() as db:
                db.add(db_book)
                db.commit()
                db.refresh(db_book)
                return db_book
        except IntegrityError:
            error: DBException = DBException()
            error.message = "Author and book pair already exists"
            raise error

    def find_one(self, book_id: str):
        with get_session() as db:
            return db.query(BookModel).filter(BookModel.uuid == book_id).first()

    def find_all(self, offset: int = 0, limit: int = 10):
        with get_session() as db:
            return db.query(BookModel).offset(offset).limit(limit).all()

    def delete_one(self, book_id: str) -> int:
        with get_session() as db:
            res = db.query(BookModel).filter(BookModel.uuid == book_id).delete()
            db.commit()
            return res
