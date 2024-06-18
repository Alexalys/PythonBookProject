from sqlalchemy.orm import Session
from app.models.Book import BookModel
from app.schemas.bookSchema import BookCreate


class Repository:
    def create_book(self, db: Session, db_book: BookModel):
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    def get_book(self, db: Session, book_id: int):
        return db.query(BookModel).filter(BookModel.id == book_id).first()

    def get_books(self, db: Session, offset: int = 0, limit: int = 10):
        return db.query(BookModel).offset(offset).limit(limit).all()
